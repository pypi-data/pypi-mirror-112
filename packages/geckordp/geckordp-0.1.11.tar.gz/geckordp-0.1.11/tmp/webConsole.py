from enum import Enum
from typing import List
from geckordp.rdpClient import RDPClient
from geckordp.actors.actor import Actor


class WebConsoleActor(Actor):
    """ https://github.com/mozilla/gecko-dev/blob/master/devtools/shared/specs/webconsole.js
    """
    
    class Listeners(str, Enum):
        """ https://github.com/mozilla/gecko-dev/blob/8859fc390700d9f3ec4e5a4f38882e05eaf657bb/devtools/server/actors/webconsole.js#L616
            Listeners != Events
        """
        PAGE_ERROR = "PageError"
        CONSOLE_API = "ConsoleAPI"
        NETWORK_ACTIVITY = "NetworkActivity"
        FILE_ACTIVITY = "FileActivity"
        REFLOW_ACTIVITY = "ReflowActivity"
        CONTENT_PROCESS_MESSAGES = "ContentProcessMessages"
        DOCUMENT_EVENTS = "DocumentEvents"

    class MessageTypes(str, Enum):
        PAGE_ERROR = "PageError"
        CONSOLE_API = "ConsoleAPI"

    def __init__(self, *args, **kwargs):
        super(WebConsoleActor, self).__init__(*args, **kwargs)

    def __del__(self):
        pass

    def start_listeners(self, listeners: List[Listeners]):
        nlisteners = []
        for listener in listeners:
            nlisteners.append(str(listener.value))
        return self.client.request_response({
            "to": self.actor_id,
            "type": "startListeners",
            "listeners": nlisteners,
        })

    def stop_listeners(self, listeners: List[Listeners]):
        nlisteners = []
        for listener in listeners:
            nlisteners.append(str(listener.value))
        return self.client.request_response({
            "to": self.actor_id,
            "type": "stopListeners",
            "listeners": nlisteners,
        })

    def get_cached_messages(self, message_types : List[MessageTypes]):
        nmessage_types = []
        for message_type in message_types:
            nmessage_types.append(str(message_type.value))
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getCachedMessages",
            "messageTypes": nmessage_types,
        })

    def evaluate_js_async(self, text: str, eager = False):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "evaluateJSAsync",
            "text": "(() => { "+ text + " })();",
            "eager": eager,
        })

    def autocomplete(self, text: str, cursor=0, frame_actor="",
                     selected_node_actor="", authorized_evaluations_json={}, expression_vars_json={}):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "autocomplete",
            "text": text,
            "cursor": cursor,
            "frameActor": frame_actor,
            "selectedNodeActor": selected_node_actor,
            "authorizedEvaluations": authorized_evaluations_json,
            "expressionVars": expression_vars_json,
        })

    def clear_messages_cache(self):
        return self.client.request({
            "to": self.actor_id,
            "type": "clearMessagesCache",
        })

    def get_preferences(self):
        # https://github.com/mozilla/gecko-dev/blob/8859fc390700d9f3ec4e5a4f38882e05eaf657bb/devtools/server/actors/webconsole.js#L1522
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getPreferences",
        })

    def set_preferences(self,
                        preferences={
                            "NetworkMonitor.saveRequestAndResponseBodies": True,
                            "NetworkMonitor.throttleData": False,
                        }):
        # https://github.com/mozilla/gecko-dev/blob/8859fc390700d9f3ec4e5a4f38882e05eaf657bb/devtools/server/actors/webconsole.js#L1536
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setPreferences",
            "preferences": preferences,
        })

    def block_request(self, url : str):
        # https://github.com/mozilla/gecko-dev/blob/6178b9bfde68881523a8a30bbc0b78eac1f95159/devtools/server/actors/network-monitor/network-observer.js#L1029
        return self.client.request_response({
            "to": self.actor_id,
            "type": "blockRequest",
            "filter": {
                "url": url,
            },
        })

    def unblock_request(self, url : str):
        # https://github.com/mozilla/gecko-dev/blob/6178b9bfde68881523a8a30bbc0b78eac1f95159/devtools/server/actors/network-monitor/network-observer.js#L1044
        return self.client.request_response({
            "to": self.actor_id,
            "type": "unblockRequest",
            "filter":{
                "url": url,
            },
        })

    # todo: causes an null error on server-side, maybe it is deprecated?
    # however the similar function NetworkContentActor works fine
    """ def send_http_request(self,
                          method: "GET",
                          url: str,
                          headers={
                              "Host": "www.duckduckgo.com",
                              "User-Agent": "my-user-agent",
                          },
                          body=""):
        nheaders = []
        for name, value in headers.items():
            nheaders.append({
                "name": name,
                "value": value,
            })
        return self.client.request_response({
            "to": self.actor_id,
            "type": "sendHTTPRequest",
            "request": {
                "cause": {
                    "type": "document",
                    "loadingDocumentUri": None,
                    "stacktraceAvailable": True,
                    "lastFrame": {},
                },
                "url": url,
                "method": method.upper(),
                "headers": nheaders,
                "body": body,
            },
        }) """

    # todo
    # see: NetworkParentActor
    # probably deprecated in the future? 
    # it doesn't seem to make a difference between
    # the two contexts
    """ 
    def set_blocked_urls(self, urls : List[str]):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "setBlockedUrls",
            "urls": urls,
        })

    def get_blocked_urls(self):
        return self.client.request_response({
            "to": self.actor_id,
            "type": "getBlockedUrls",
        })
    """
