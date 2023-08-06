    def visit(self, to : str, url : str):
        with self.__mtx:
            return self.__init_request({
                "to": f"{to}",
                "type": "sendHTTPRequest",
                "request": {
                    "url": f"{url}",
                    "method": "GET",
                    "headers": {
                        "name": "Header-name",
                        "value": "header value",
                    },
                }
            })

    def evaluate_js(self, to : str, cmd : str):
        with self.__mtx:
            return self.__init_request({
                "to": f"{to}",
                "type": "evaluateJS",
                "text": f"{cmd}",
                "bindObjectActor": "null",
                "frameActor": "null",
                "url": "null",
                "selectedNodeActor": "null",
            })


    @property
    def current_tab(self):
        tabs = self.list_tabs()
        for tab in tabs:
            if tab["selected"]:
                return tab

    @property
    def current_console(self):
        tabs = self.list_tabs()
        for tab in tabs:
            if tab["selected"]:
                return tab


    def listen(self, event_type : ListenEvents, handler):
        """ Listen to an remote host event. 
            
            Example:

            def myfunc(result : {})
                print(result)

            RDPClient.listen(ListenEvents.pageError, myfunc)
        """
        with self.__mtx:
            self.__event_handlers[event_type.name] = handler
            """ self.__request({
                "to": "conn0.console9",
                "type": "startListeners",
                "listeners": [
                    "PageError",
                    "ConsoleAPI",
                    "NetworkActivity",
                    "FileActivity"
                ]
            }) """



    def get_root(self):
        with self.__mtx:
            return self.__init_request({
                "to": "root",
                "type": "getRoot"
            })

    def list_tabs(self):
        with self.__mtx:
            return self.__init_request({
                "to": "root",
                "type": "listTabs"
            })["tabs"]

    def get_target(self, tabdescriptor : str):
        with self.__mtx:
            return self.__init_request({
                "to": f"{tabdescriptor}",
                "type": "getTarget"
            })


    # CHECK RDPCLIENT __READ
    # TODO DECODE ONLY AFTER MESSAGE HAS BEEN COMPLETED TO GET THE CORRECT SIZE, SINCE
    # ENCODING DOES CHANGING THE SIZE
    """ response = bytearray(2)
    response[0] = 0x1
    response[1] = 0x1 """

    """ response = bytes([0x68, 0xc3, 0x88, 0x6c, 0x6c, 0x6f])

    read_buffer = bytearray(10)
    memcpy(read_buffer, 2, response, len(response))


    view = memoryview(read_buffer)
    view2 = memoryview(read_buffer[0:6])
    string = str(view, "utf-8")
    string2 = view.tobytes().decode(encoding="utf-8")
    bb = view.tobytes()
    #bbb = view[2:8].tobytes()
    #cbuf = ctypes.create_string_buffer(response)
    #print(cbuf.raw)
    #print(ctypes.string_at(cbuf))


    print(hex(id(view[0])))
    print(hex(id(view2[0])))
    print(hex(id(read_buffer[0])))
    print(hex(id(string[0])))
    print(hex(id(bb[0])))
    print(bb)
    


    print(''.join('0x{:02x} '.format(x) for x in view))
    print(''.join('0x{:02x} '.format(x) for x in view2))
    return """

    """ print(bb[9])
    print(sys.getsizeof(bb))
    print(sys.getsizeof(bb)) """
    """ print(len(bb))
    bb.append(0x25)
    print(len(bb)) """

    """ with RDPClient(timeout_sec=3, host="localhost", port=6000) as cl:
        log(f"----------------------{cl.connect('localhost', 6000) == None}")
        cl.disconnect()
        #sleep(5)
        log(f"----------------------{cl.connect('localhost', 6000) == None}")
        cl.disconnect()
        #sleep(5)
        log(f"----------------------{cl.connect('localhost', 6000) == None}") """

    """ with RDPClient(timeout_sec=0.7) as cl:
        sleep(5)
        logdict(cl.connect("localhost", 6000))
        sleep(5) """

    """ with open('jj.json',mode='r') as f:
        text = f.read()
        ff = json.loads(text, strict=False)
    return """


    """ tab = TabActor(cl, current_tab["actor"])

    browser = BrowsingContextActor(cl, descriptors["actor"])
    browser.attach()
    console = WebConsoleActor(cl, descriptors["consoleActor"])
    listeners = []
    for listen in WebConsoleActor.Listeners:
        listeners.append(listen.name)
    console.start_listeners(listeners)

    def doc_handler(data):
        log(data)

    cl.add_listen(descriptors["consoleActor"], WebConsoleActor.Events.documentEvent, doc_handler)

    browser.navigate_to("https://www.heise.de/") """

    #sleep(2)
    #log("___________________________________\n\n")
    #browser.navigate_to("https://www.heise.de/")

    #cl.disconnect()

    """ console = WebConsoleActor(cl, descriptors["consoleActor"])
    console.start_listeners(
        ["PageError", "ConsoleAPI"])
    logdict(descriptors) """
    return
    logdict(console.evaluate_js_sync(""" 

        function mult() {
            return 23;
        }

        console.log('lolllllololol');
        return 6 * mult();


    """))
    logdict(console.evaluate_js_sync(""" 

        //import { DevToolsUtils } from "devtools-modules";
        //DevToolsUtils.saveAs(window, "bla", test.txt);
        //var gg = require("devtools-modules")
        //return true

        /*var jq = document.createElement('script');
        jq.src = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js";
        document.getElementsByTagName('head')[0].appendChild(jq);
        // ... give time for script to load, then type (or see below for non wait option)
        jQuery.noConflict();
        return 12;*/

        var jq = document.createElement('script');
        jq.type = "module";

        jq.innerHTML = `
        


        `


        document.getElementsByTagName('head')[0].appendChild(jq);
        return 10;


    """))

    #cl.disconnect()
