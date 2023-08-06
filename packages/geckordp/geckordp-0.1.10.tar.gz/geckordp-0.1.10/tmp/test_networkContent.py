import pytest
import tests.helpers.utils as utils
import tests.helpers.constants as constants
from geckordp.rdpClient import RDPClient
from geckordp.actors.root import RootActor
from geckordp.actors.descriptors.tab import TabActor
from geckordp.actors.networkContent import NetworkContentActor
from geckordp.actors.webConsole import WebConsoleActor
from geckordp.actors.targets.browsingContext import BrowsingContextActor
from geckordp.actors.watcher import WatcherActor
from geckordp.actors.events import Events
from geckordp.logger import log, logdict
from time import sleep

def init():
    cl = RDPClient(3)
    cl.connect(constants.remote_host, constants.remote_port)
    root = RootActor(cl)
    current_tab = root.current_tab()
    tab = TabActor(cl, current_tab["actor"])
    actor_ids = tab.get_target()
    network_content = NetworkContentActor(cl, actor_ids["networkContentActor"])
    browser = BrowsingContextActor(cl, actor_ids["actor"])
    console = WebConsoleActor(cl, actor_ids["consoleActor"])
    watcher = WatcherActor(cl, tab.get_watcher()["actor"])
    return cl, network_content, browser, console, watcher


def test_send_http_request():
    cl = None
    try:
        cl, console = init()
        console.start_listeners([])
        val = console.send_http_request(
            method="GET",
            url="https://example.com/",
            headers={
                "Host": "example.com",
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": 1,
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": 1,
            },
            body="")
        logdict(val)
        # response is null error on server-side, probably wrong actor or deprecated in webconsole
    finally:
        cl.disconnect()
        
""" def test_send_http_request():
    cl = None
    try:
        cl, network_content, _, _ = init()
        val = network_content.send_http_request(
            method="GET",
            url="https://example.com/",
            headers={
                "Host": "example.com",
                "User-Agent": "special-agent-007"
            },
            body="my name is bond, james bond")["channelId"]
        assert val > 0
    finally:
        cl.disconnect() """


channel_id = 0

def on_resource_available(data):
    resources = data["resources"]
    if (len(resources) <= 0):
        return
    resources = resources[0]
    if (resources["resourceType"] != "network-event"):
        return
    resource_id = resources.get("resourceId", -1)
    log(channel_id)
    #assert resource_id == channel_id

def test_get_stack_trace():
    cl = None
    try:
        cl, network_content, browser, console, watcher = init()
        



        cl.add_event_listener(
            watcher.actor_id,
            Events.Watcher.RESOURCE_AVAILABLE_FORM,
            on_resource_available)
        #browser.attach()
        #console.start_listeners([])
        watcher.watch_resources(
            [WatcherActor.Resources.NETWORK_EVENT_STACKTRACE,
             WatcherActor.Resources.NETWORK_EVENT])

        global channel_id
        channel_id = network_content.send_http_request(
            method="GET",
            url="https://example.com/",
            headers={
                "Host": "example.com",
                "User-Agent": "special-agent-007"
            },
            body="my name is bond, james bond")["channelId"]
        log(channel_id)

        val = network_content.get_stack_trace(channel_id)
        logdict(val)
    finally:
        cl.disconnect()

