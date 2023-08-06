import asyncio
import socket
from enum import Enum
from threading import Thread, Lock
import json
from concurrent.futures import Future
from queue import Queue
from time import sleep
from geckordp.config import g_is_debug
from geckordp.logger import log, dlog, elog


class RDPClient():

    def __init__(self, timeout_sec=3, host="", port=0, max_read_size=65536):
        """ Initializes an instance of the remote debug protocol client.

        Requirements:
            "firefox --start-debugger-server 6000"
            firefox -> url -> about:config -> devtools.debugger.remote-enabled
            firefox -> url -> about:config -> devtools.chrome.enabled
            firefox -> url -> about:config -> devtools.debugger.prompt-connection
            firefox -> url -> about:config -> browser.sessionstore.resume_from_crash

        Args:
            timeout_sec (int, optional): The timeout for a response in seconds. Defaults to 3.
            host (str, optional): The host to connect to. This will be only used if the keyword 'with:' is used. Defaults to "".
            port (int, optional): The port to use. This will be only used if the keyword 'with:' is used. Defaults to 0.
        """
        self.__ENCODING = "utf-8"
        self.__READ_SINGLE_DIGITS = 8
        self.__MAX_READ_SIZE = max_read_size
        self.__READ_FALLBACK_SIZE = max_read_size
        self.__timeout_sec = timeout_sec
        self.__host = host
        self.__port = port
        self.__mtx = Lock()
        self.__connect_mtx = Lock()
        self.__loop = asyncio.new_event_loop()
        self.__loop_thread = None
        self.__reader = None
        self.__writer = None
        self.__connected = False
        self.__fut = None
        self.__dc_fut = None
        self.__recv_from = ""
        self.__read_task = None
        self.__cached_response = ""
        self.__cached_buffer_read = 0
        self.__cached_total_size = 0
        self.__registered_events = set()    # type: List[str]
        self.__event_handlers = {}          # type: Dict[event : str, Dict[actor_id : str, List[handler]]]

    def __del__(self):
        pass

    def __enter__(self):
        self.connect(self.__host, self.__port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    @property
    def timeout_sec(self) -> int:
        """ Returns the timeout in seconds.

        Returns:
            int: The timeout.
        """
        return self.__timeout_sec

    def register_events(self, events: Enum):
        """ Register events for the event handler.

        Args:
            events (Enum): The "Events" class within the derived "Actor" class.
        """
        with self.__mtx:
            for event in events:
                self.__registered_events.add(event.name)

    def add_listen(self, actor_id : str, event, handler):
        """ Appends a callback handler and listen to the specified event.
        Multiple handlers can be added for each event type.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class.
            handler (any): The handler to call on desired events.
        """
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.name
        with self.__mtx:
            # check if event is in dict and create another dict as value entry
            if (not event_name in self.__event_handlers):
                self.__event_handlers[event_name] = {}
            # check if actor id is in the next dict and create the list for the handlers
            if (not actor_id in self.__event_handlers[event_name]):
                self.__event_handlers[event_name][actor_id] = []
            self.__event_handlers[event_name][actor_id].append(handler)

    def del_listen(self, actor_id : str, event, handler):
        """ Removes a callback handler from the specified event.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class
            handler (any): The handler to call on desired events.
        """
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.name
        with self.__mtx:
            if (not event_name in self.__event_handlers):
                return
            if (not actor_id in self.__event_handlers[event_name]):
                return
            self.__event_handlers[event_name][actor_id].remove(handler)

    def connect(self, host: str, port: int) -> dict:
        """ Connects to the firefox debug server.

        Args:
            host (str): The host to connect to, usually 'localhost'
            port (int): The port to use, default '6000'

        Returns:
            dict/None: The server response on successful established connection.
        """
        with self.__mtx:
            if (self.__connected):
                return None
            dlog("")
            self.__fut = Future()
            self.__loop_thread = Thread(
                target=self.__connect, args=[host, port])
            self.__loop_thread.start()
            try:
                return self.__fut.result(self.__timeout_sec)
            except:
                dlog("Timeout")
                if (len(asyncio.all_tasks(self.__loop)) > 0):
                    dlog("Cancel read")
                    self.__loop.call_soon_threadsafe(
                        asyncio.ensure_future, self.__disconnect())
            return None

    def __connect(self, host: str, port: int):
        if (self.__loop.is_running()):
            log("Queue is already running")
            return
        dlog("Queue read task")
        self.__read_task = self.__loop.create_task(
            self.__open_connection(host, port))
        self.__read_task.add_done_callback(self.__on_close_connection)
        try:
            dlog("Run IO loop")
            self.__loop.run_until_complete(self.__read_task)
        except asyncio.exceptions.CancelledError:
            dlog("Read task cancelled")
        except socket.gaierror as e:
            elog(f"{e}")

    def connected(self):
        with self.__mtx:
            return self.__connected

    async def __open_connection(self, host: str, port: int):
        dlog("Try to open connection")
        try:
            self.__reader = asyncio.StreamReader(
                limit=self.__MAX_READ_SIZE, loop=self.__loop)
            protocol = asyncio.StreamReaderProtocol(
                self.__reader, loop=self.__loop)
            transport, _ = await self.__loop.create_connection(
                lambda: protocol, host, port)
            self.__writer = asyncio.StreamWriter(
                transport, protocol, self.__reader, self.__loop)
        except ConnectionRefusedError as e:
            elog(e)
            return
        dlog("Start listening")
        self.__connected = True
        await self.__read()

    def __on_close_connection(self, future):
        try:
            dlog("Stop listening")
            self.__connected = False
            self.__dc_fut.set_result(1)
        except:
            pass

    def disconnect(self):
        """ Disconnect from the debug server.
        """
        with self.__mtx:
            if (not self.__connected):
                return
            dlog("")
            self.__dc_fut = Future()
            self.__loop.call_soon_threadsafe(
                asyncio.ensure_future, self.__disconnect())
            try:
                self.__dc_fut.result(0.2)
                return
            except:
                dlog("Timeout")
            return

    async def __disconnect(self):
        dlog(self.__connected)
        self.__read_task.cancel()

    def request(self,  msg: dict) -> dict:
        """ Starts sending a request without waiting for a response.
        The dict message will be transformed to a utf-8 json string.

        Args:
            msg (dict): The message to send.

        """
        with self.__mtx:
            if (not self.__connected):
                return
            dlog("")
            self.__loop.call_soon_threadsafe(
                asyncio.ensure_future, self.__request(msg))

    def request_response(self,  msg: dict) -> dict:
        """ Starts sending a request and waiting for a response.
        The dict message will be transformed to a utf-8 json string.
        The timeout can be specified in the class its constructor.

        Args:
            msg (dict): The message to send.

        Returns:
            dict/None: The response from the server.
        """
        with self.__mtx:
            if (not self.__connected):
                return None
            dlog("")
            if ("to" in msg):
                self.__recv_from = msg["to"]
            else:
                dlog("Field 'to' doesn't exist")
                self.__recv_from = ""
            self.__fut = Future()
            self.__loop.call_soon_threadsafe(
                asyncio.ensure_future, self.__request(msg))
            try:
                return self.__fut.result(self.__timeout_sec)
            except:
                dlog("Timeout")
                return None

    async def __request(self, msg: dict):
        msg = json.dumps(msg, separators=(',', ':'))
        self.__writer.write(
            bytes(f"{len(msg)}:{msg}", encoding=self.__ENCODING))
        await self.__writer.drain()

    async def __read(self):
        while True:
            # read first the size of the response if possible then the complete message
            # calls to the reader will keep the connection open (useful for listener events)
            # if finding the size was successful it will return the size and an empty string,
            # else it will fallback to a big size and the read string data
            read_size, json_response = await self.__read_size()
            json_response += (await self.__reader.read(read_size)).decode(self.__ENCODING)
            buffer_read = len(json_response)

            # complete the message received from the server if too big
            # there seems to be a limitation in the socks implementation 
            # itself which limits it to ~64kb
            if (buffer_read < read_size and self.__cached_total_size == 0):
                # cache_total_size is the size of the message itself without
                # the size indicator at the start for e.g. 54651:{...}
                self.__cached_total_size = read_size
                self.__cached_buffer_read = buffer_read
                self.__cached_response = json_response
                dlog(
                    f"message to large [{self.__cached_buffer_read} < {self.__cached_total_size}]")
                continue
            if (self.__cached_total_size > 0):
                self.__cached_buffer_read += buffer_read
                self.__cached_response += json_response
                if (self.__cached_buffer_read < self.__cached_total_size):
                    dlog(
                        f"read more [{self.__cached_buffer_read} < {self.__cached_total_size}]")
                    continue
                elif (self.__cached_buffer_read >= self.__cached_total_size):
                    dlog(
                        f"read finished [{self.__cached_buffer_read} >= {self.__cached_total_size}]")
                    json_response = self.__cached_response




            if (not json_response):
                elog(f"EOF remote host closed")
                return
            response = None
            try:
                response = json.loads(json_response, strict=False)
            except:
                elog(
                    f"couldn't load json response as dictionary:\n'{json_response}'")
                continue

            if (g_is_debug):
                dlog(f"\n{response}")

            # check if listener event
            if (self.__handle_events(response)):
                continue
            """ if ("type" in response):
                event_name = response["type"]
                if ("from" in response):
                    actor_id = response["from"]
                    # check if event exists and if handler is assigned
                    actors = self.__event_handlers.get(event_name, None)
                    if (actors):
                        handlers = actors.get(actor_id, None)
                        if (handlers):
                            for handler in handlers:
                                if (handler):
                                    handler(response)
                        dlog(f"event received")
                        continue
                # check if event is registered and avoid unhandled further execution
                if (event_name in self.__registered_events):
                    dlog(f"unhandled event received")
                    continue """
                
            self.__handle_response(response)
            # if future object is set from public functions, trigger it
            """ if (self.__fut):
                skip = True
                # if receiver is set, check it in response
                if (self.__recv_from and "from" in response and response["from"] == self.__recv_from):
                    skip = False
                # else if receiver is not set, the caller is not expecting a "from" field in response
                elif (not self.__recv_from):
                    skip = False
                    dlog(f"field 'from' doesn't exist in response")
                # set future and release the waiting function
                if (not skip):
                    try:
                        dlog("response valid, set result")
                        self.__fut.set_result(response)
                    except:
                        pass """


    def __handle_events(self, response : dict):
        if ("type" in response):
            event_name = response["type"]
            if ("from" in response):
                actor_id = response["from"]
                # check if event exists and if handler is assigned
                actors = self.__event_handlers.get(event_name, None)
                if (actors):
                    handlers = actors.get(actor_id, None)
                    if (handlers):
                        for handler in handlers:
                            if (handler):
                                handler(response)
                    dlog(f"event received")
                    return True
            # check if event is registered and avoid unhandled further execution
            if (event_name in self.__registered_events):
                dlog(f"unhandled event received")
                return True
        return False

    def __handle_response(self, response: dict):
        if (self.__fut):
            skip = True
            # if receiver is set, check it in response
            if (self.__recv_from and "from" in response and response["from"] == self.__recv_from):
                skip = False
            # else if receiver is not set, the caller is not expecting a "from" field in response
            elif (not self.__recv_from):
                skip = False
                dlog(f"field 'from' doesn't exist in response")
            # set future and release the waiting function
            if (not skip):
                try:
                    dlog("response valid, set result")
                    self.__fut.set_result(response)
                except:
                    pass

    async def __read_size(self):
        size_str = ""
        read_str = ""
        # read the first few bytes of the response to get the payload size
        # the actual response look something like this:
        # 196:{"x":"y"}
        for _ in range(0, self.__READ_SINGLE_DIGITS):
            char = (await self.__reader.read(1)).decode(self.__ENCODING)
            read_str += char
            if char.isnumeric():
                size_str += char
                continue
            # check if the specified size ends with a colon
            if (char == ":"):
                try:
                    return int(size_str), ""
                except:
                    dlog(f"could not convert '{size_str}' to integer")
                    return self.__READ_FALLBACK_SIZE, read_str
        dlog(
            f"No size specified at the beginning of the response '{size_str}'")
        return self.__READ_FALLBACK_SIZE, read_str
        #return 0, read_str
