from typing import List, Dict, Callable, Any
from . import util as plugin_util


class PyriWebUIServerPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self) -> str:
        return ""

    def get_plugin_route_handler(self) -> Callable[["sanic.request.Request",str],"sanic.response.BaseHTTPResponse"]:
        return None

def get_webui_server_plugin_factories() -> List[PyriWebUIServerPluginFactory]:
    return plugin_util.get_plugin_factories("pyri.plugins.webui_server")

def get_all_webui_server_route_handlers() -> Dict[str,Any]:
    ret = dict()
    factories = get_webui_server_plugin_factories()
    for factory in factories:
        ret[factory.get_plugin_name()] = factory.get_plugin_route_handler()

    return ret