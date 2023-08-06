import asyncio
from enum import Enum
from threading import Thread, Lock
import json
import concurrent
from queue import Queue
from time import sleep
from remotefox.config import g_is_debug
from remotefox.logger import log, dlog, elog

class RDPClient():

    def __init__(self, timeout_sec = 3, host="", port=0):
        """ Initializes an instance of the remote debug protocol client.
        Requirements:
            "firefox --start-debugger-server 6000"
            firefox -> url -> about:config -> devtools.debugger.remote-enabled
            firefox -> url -> about:config -> devtools.chrome.enabled
            firefox -> url -> about:config -> devtools.debugger.prompt-connection

        Args:
            timeout_sec (int, optional): The timeout for a response in seconds. Defaults to 3.
            host (str, optional): The host to connect to. This will be only used if the keyword 'with:' is used. Defaults to "".
            port (int, optional): The port to use. This will be only used if the keyword 'with:' is used. Defaults to 0.
        """
        self.__ENCODING = "utf-8"
        self.__MAX_STR_SIZE = 8
        self.__READ_FALLBACK_SIZE = 65536
        self.__timeout_sec = timeout_sec
        self.__host = host
        self.__port = port
        self.__mtx = Lock()
        self.__loop = asyncio.new_event_loop()
        self.__loop_thread = None
        self.__reader = None
        self.__writer = None
        self.__connected = False
        self.__fut = None
        self.__recv_from = ""
        self.__read_task = None
        self.__registered_events = set()   # type: List[str]
        self.__event_handlers = {}      # type: Dict[Enum, List[Func]]
        
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

    def register_events(self, events : Enum):
        """ Register events for the event handler.

        Args:
            events (Enum): The "Events" class within the derived "Actor" class.
        """
        with self.__mtx:
            for event in events:
                self.__registered_events.add(event.name)

    def add_listen(self, event, handler):
        """ Appends a callback handler and listen to the specified event.
        Multiple handlers can be added for each event type.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class.
            handler (any): The handler to call on desired events.
        """
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.name
        #dlog(event_name)
        with self.__mtx:
            if (not event_name in self.__event_handlers):
                self.__event_handlers[event_name] = []
            self.__event_handlers[event_name].append(handler)

    def del_listen(self, event, handler):
        """ Removes a callback handler from the specified event.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class
            handler (any): The handler to call on desired events.
        """
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.name
        #dlog(event_name)
        with self.__mtx:
            if (not event_name in self.__event_handlers):
                return
            self.__event_handlers[event_name].remove(handler)

    def connect(self, host: str, port: int) -> dict:
        """ Connects to the firefox debug server.

        Args:
            host (str): The host to connect to, usually 'localhost'
            port (int): The port to use, default '6000'

        Returns:
            dict/None: The server response on successful established connection.
        """
        with self.__mtx:
            self.__fut = concurrent.futures.Future()
            if (self.__connected):
                return
            dlog("")
            self.__loop_thread = Thread(
                target=self.__connect, args=[host, port])
            self.__loop_thread.start()
            try:
                return self.__fut.result(self.__timeout_sec)
            except:
                dlog("Timeout")
            return None

    def __connect(self, host: str, port: int):
        dlog("Queue read task")
        self.__read_task = self.__loop.create_task(
            self.__open_connection(host, port))
        try:
            dlog("Run IO loop")
            self.__loop.run_until_complete(self.__read_task)
        except asyncio.exceptions.CancelledError:
            dlog("Read task cancelled")
            self.__connected = False

    async def __open_connection(self, host : str, port : int):
        dlog("Try to open connection")
        try:
            # todo deprecated, see function itself
            self.__reader, self.__writer = await asyncio.open_connection(
                host=host, port=port, loop=self.__loop)
        except ConnectionRefusedError as e:
            elog(e)
            return
        except:
            elog("unhandled exception")
            return
        dlog("Listen for server messages now")
        self.__connected = True
        await self.__read()

    def disconnect(self):
        """ Disconnect from the debug server.
        """
        with self.__mtx:
            if (not self.__connected):
                return
            dlog("")
            self.__connected = False
            self.__loop.call_soon_threadsafe(
                asyncio.ensure_future, self.__disconnect())

    async def __disconnect(self):
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
            self.__fut = concurrent.futures.Future()
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
            read_size = await self.__read_size()
            json_response = (await self.__reader.read(read_size)).decode(self.__ENCODING)
            response = None
            try:
                response = json.loads(json_response)
            except:
                elog(
                    f"couldn't load json response as dictionary:\n{json_response}")
                continue

            if (g_is_debug):
                dlog(f"\n{response}")

            # check if listener event
            if ("type" in response):
                event_name = response["type"]
                # check if event exists and if handler is assigned
                if (event_name in self.__event_handlers):
                    dlog(f"event received")
                    for handler in self.__event_handlers[event_name]:
                        if (handler):
                            handler(response)
                    continue
                # check if event is registered and avoid unhandled further execution
                if (event_name in self.__registered_events):
                    dlog(f"unhandled event received")
                    continue

            # if future object is set from public functions, trigger it
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
        # read the first few bytes of the response to get the payload size
        # the actual response look something like this:
        # 196:{"x":"y"}
        for _ in range(0, self.__MAX_STR_SIZE):
            char = (await self.__reader.read(1)).decode(self.__ENCODING)
            if char.isnumeric():
                size_str += char
                continue
            # check if the specified size ends with a colon
            if (char == ":"):
                try:
                    return int(size_str)
                except:
                    dlog(f"could not convert '{size_str}' to integer")
                    return self.__READ_FALLBACK_SIZE
        dlog(f"No size specified at the beginning of the response '{size_str}'")
        return 0
