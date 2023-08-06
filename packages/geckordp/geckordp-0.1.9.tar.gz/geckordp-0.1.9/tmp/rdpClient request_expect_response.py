import asyncio
import socket
from time import time
from enum import Enum
from threading import Thread, Lock
import json
import collections
from concurrent.futures import Future
from queue import Queue
from time import sleep
from typing import List
from geckordp.config import g_is_debug, g_debug_events, g_debug_response
from geckordp.logger import log, dlog, elog
from geckordp.buffers import LinearBuffer


class RequestEntry():

    def __init__(self, timeout_sec: int, to: str, expect_nested_field : []):
        self.timestamp = time()
        self.future = Future()
        self.timeout_sec = timeout_sec
        self.to = to
        self.expect_nested_field = expect_nested_field


class RDPClient():

    def __init__(self, timeout_sec=3, host="", port=0):
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
        self.__MAX_READ_SIZE = 65536
        self.__NUMBER_LUT = bytes([0x30, 0x31, 0x32, 0x33, 0x34,
                            0x35, 0x36, 0x37, 0x38, 0x39])
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
        self.__dc_fut = None
        self.__read_task = None
        self.__cached_response = ""
        self.__cached_buffer_read = 0
        self.__cached_total_size = 0
        self.__digits_buffer = LinearBuffer(self.__READ_SINGLE_DIGITS)
        self.__read_buffer = LinearBuffer(1048576)
        self.__registered_events = set()    # type: List[str]

        self.__await_request_mtx = Lock()
        self.__await_request = collections.defaultdict(list)  # type: Dict[from : str, List[RequestEntry]]
        self.__await_single_request = RequestEntry(0, "", [])

        self.__event_mtx = Lock()
        self.__event_handlers = {}  # Dict[event : str, Dict[actor_id : str, List[handler]]]

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
                self.__registered_events.add(event.value)

    def add_handler(self, actor_id: str, event, handler):
        """ Appends a callback handler and listen to the specified event.
        Multiple handlers can be added for each event type.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class.
            handler (any): The handler to call on desired events.
        """
        with self.__event_mtx:
            self.__add_handler(actor_id, event, handler)

    def __add_handler(self, actor_id: str, event, handler):
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.value
        # check if event is in dict and create another dict as value entry
        if (not event_name in self.__event_handlers):
            self.__event_handlers[event_name] = {}
        # check if actor id is in the next dict and create the list for the handlers
        if (not actor_id in self.__event_handlers[event_name]):
            self.__event_handlers[event_name][actor_id] = []
        self.__event_handlers[event_name][actor_id].append(handler)

    def del_handler(self, actor_id: str, event, handler):
        """ Removes a callback handler from the specified event.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class
            handler (any): The handler to call on desired events.
        """
        with self.__event_mtx:
            self.__del_handler(actor_id, event, handler)

    def __del_handler(self, actor_id: str, event, handler):
        """ Removes a callback handler from the specified event.

        Args:
            event_type (Enum/str): The event type, usually found within the derived actor class
            handler (any): The handler to call on desired events.
        """
        event_name = event
        if (isinstance(event, Enum)):
            event_name = event.value
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
            self.__await_single_request.to = "root"
            self.__await_single_request.future = Future()
            self.__loop_thread = Thread(
                target=self.__connect, args=[host, port])
            self.__loop_thread.start()
            try:
                return self.__await_single_request.future.result(self.__timeout_sec)
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
                elog(f"Not connected on request:\n{msg}")
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
                elog(f"Not connected on request:\n{msg}")
                return None
            dlog("")
            if (not "to" in msg):
                raise ValueError("parameter 'msg' must contain 'to' field")
            self.__await_single_request.to = msg["to"]
            self.__await_single_request.future = Future()
            self.__loop.call_soon_threadsafe(
                asyncio.ensure_future, self.__request(msg))
            try:
                response = self.__await_single_request.future.result(
                    self.__timeout_sec)
                if ("error" in response):
                    elog(f"Error on request:\n{msg}")
                return response
            except:
                elog(f"Timeout on request:\n{msg}")
                return None

    def request_expect_response(self,  msg: dict, *expect_nested_field) -> dict:
        """ Starts sending a request, queues a response object with a 
            specific nested field marking and waiting for a response.
        The dict message will be transformed to a utf-8 json string.
        The timeout can be specified in the class its constructor.

        Args:
            msg (dict): The message to send.

        Returns:
            dict/None: The response from the server.
        """
        with self.__mtx:
            if (not self.__connected):
                elog(f"Not connected on request:\n{msg}")
                return None

        # prepare data to be queued
        dlog("")
        if (not "to" in msg):
            raise ValueError("parameter 'msg' must contain 'to' field")
        to_actor = msg["to"]
        response = RequestEntry(
            self.__timeout_sec, to_actor, list(expect_nested_field))

        # queue to list
        with self.__await_request_mtx:
            self.__await_request[to_actor].append(response)
            
        # send request to server and wait for response
        self.__loop.call_soon_threadsafe(
            asyncio.ensure_future, self.__request(msg))
        try:
            response = response.future.result(self.__timeout_sec)
            if ("error" in response):
                elog(f"Error on request:\n{msg}")
            return response
        except:
            elog(f"Timeout on request:\n{msg}")
            return None

    async def __request(self, msg: dict):
        msg = json.dumps(msg, separators=(',', ':'))
        self.__writer.write(
            bytes(f"{len(msg)}:{msg}", encoding=self.__ENCODING))
        await self.__writer.drain()

    async def __read(self):
        while True:
            # read a few single digits to get the actual size of the response:
            # at the beginning of every server message there is a size indicator
            # it does look like this:
            # 196:{"x":"y"}
            payload_size = 0
            self.__digits_buffer.clear()
            for _ in range(0, self.__READ_SINGLE_DIGITS):
                byte = (await self.__reader.read(1))[0]
                if (self.__is_numeric(byte)):
                    self.__digits_buffer.append_byte(byte)
                    continue
                if (byte == 0x3a): # ":"
                    self.__digits_buffer.append_byte(byte)
                    payload_size = int(self.__digits_buffer.buffer(
                    ).tobytes().decode(encoding="utf-8").split(':', 1)[0])
                    break
                read_size_str = self.__digits_buffer.buffer(
                ).tobytes().decode(encoding="utf-8")
                elog(f"invalid size indicator starts with '{read_size_str}'")
                break

            # this shouldn't happen
            if (payload_size == 0):
                elog(f"remote host sent invalid response without size indicator")
                return

            # read until message is complete
            bytes_read = 0
            self.__read_buffer.reset()
            while bytes_read < payload_size:

                # truncate read size, else it will leak the next message
                trunc_read_size = payload_size - bytes_read
                # the passed max limit in streamreader doesn't seem to affect here
                if (trunc_read_size > self.__MAX_READ_SIZE):
                    trunc_read_size = self.__MAX_READ_SIZE

                read_bytes = (await self.__reader.read(trunc_read_size))
                read_bytes_size = len(read_bytes)
                if (read_bytes_size == 0):
                    elog(f"EOF remote host probably closed")
                    return
                bytes_read += read_bytes_size
                if (not self.__read_buffer.append_buffer(read_bytes)):
                    elog(
                        f"buffer overflow while appending response: buffer is too small\nbuffer:{self.__read_buffer.buffer_size()}\nresponse:{read_bytes_size}")
                    return
                if (bytes_read < payload_size):
                    dlog(f"read more data ({bytes_read} < {payload_size})")
                elif (bytes_read == payload_size):
                    dlog(f"message complete ({bytes_read} == {payload_size})")
                elif (bytes_read > payload_size):
                    dlog(f"message corrupted ({bytes_read} > {payload_size})")

            # add null termination else buffer_null_terminated() doesn't work correctly
            if (not self.__read_buffer.append_byte(0x00)):
                elog(f"buffer overflow while appending null termination")
                return

            # get string representation of bytes
            json_response = self.__read_buffer.buffer_null_terminated(
            ).tobytes().decode(encoding="utf-8")

            # load json string to dictionary
            response = None
            try:
                response = json.loads(json_response, strict=False)
            except:
                elog(
                    f"couldn't load json response as dictionary:\n'{json_response}'")
                continue
            if (g_debug_response):
                log(f"\n{json.dumps(response, indent=2)}")

            # check required response fields
            from_actor = response.get("from", None)
            if (not from_actor):
                elog(
                    f"'from' field doesn't exist in response:\n{json.dumps(response, indent=2)}")
                continue

            # check if listener event
            if (self.__handle_events(response, from_actor)):
                continue

            # handle awaiting requests
            if (self.__handle_await_requests(response, from_actor)):
                continue

            # handle single request
            self.__handle_single_request(response, from_actor)

    def __handle_events(self, response: dict, from_actor: str):
        event_type = response.get("type", None)
        if (event_type):
            if (g_debug_events):
                log(f"EVENT:\n{json.dumps(response, indent=2)}")
            # check if event exists and whether handler is assigned
            with self.__event_mtx:
                actors = self.__event_handlers.get(event_type, None)
                if (actors):
                    handlers = actors.get(from_actor, None)
                    if (handlers):
                        for handler in handlers:
                            if (handler):
                                handler(response)
                    dlog(f"event received")
                    return True
            # check if event is registered and avoid unhandled further execution
            if (event_type in self.__registered_events):
                dlog(f"unhandled event received")
                return True
        return False

    def __handle_await_requests(self, response: dict, from_actor: str):
        with self.__await_request_mtx:
            found = False
            # check if actor exist
            entries = self.__await_request.get(from_actor, None)
            if (not entries):
                return False
            # iterate entries and check whether the requested nested key exist
            for i, entry in enumerate(entries):
                if (entry.to == from_actor and self.__keys_exist(response, entry.expect_nested_field)):
                    found = True
                    try:
                        dlog("response valid, set result")
                        entry.future.set_result(response)
                    except:
                        pass
                    del entries[i]
                    break
            # remove old entries within actor
            for actor_id, v in self.__await_request.items():
                dlog(f"{actor_id} size:{len(v)}")
                v[:] = [entry for entry in v if ((time() - entry.timestamp) < entry.timeout_sec)]
                dlog(f"{actor_id} size:{len(v)}")
            # remove actors with no entries
            for k, v in list(self.__await_request.items()):
                if len(v) == 0:
                    del self.__await_request[k]
            dlog(f"__await_request size:{len(self.__await_request)}")
            return found

    def __handle_single_request(self, response: dict, from_actor: str):
        if (self.__await_single_request.future):
            if (from_actor == self.__await_single_request.to):
                try:
                    dlog("response valid, set result")
                    self.__await_single_request.future.set_result(response)
                except:
                    pass

    def __is_numeric(self, byte):
        return byte in self.__NUMBER_LUT

    def __keys_exist(self, element, keys : []):
        """
        Check if *keys (nested) exists in `element` (dict).
        https://stackoverflow.com/questions/43491287/elegant-way-to-check-if-a-nested-key-exists-in-a-dict
        """
        _element = element
        for key in keys:
            # sometimes dictionaries got also a list, so get the passed list object -> [0] 
            # and try to access it with the given index
            # for example:
            # __keys_exist(response, ["headers", [0], "name"]) = True
            """ 
            {
                "headers": [
                    {
                    "name": "Host",
                    "value": "www.google.com"
                    },
                    {
                    "name": "User-Agent",
                    "value": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"
                    },
                ],
                "headersSize": 0,
                "from": "server1.conn26.netEvent42"
            }
            """
            if isinstance(key, list) and len(key) > 0:
                try:
                    _element = _element[key[0]]
                except KeyError:
                    return False
                except IndexError:
                    return False
            else:
                try:
                    _element = _element[key]
                except KeyError:
                    return False
        return True





