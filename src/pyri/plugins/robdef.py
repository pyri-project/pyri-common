
from typing import List, Dict, TYPE_CHECKING
from importlib.metadata import entry_points
import re
import warnings

class PyriRobDefPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return ""

    def get_robdef_names(self) -> List[str]:
        return []

    def get_robdefs(self) -> List[str]:
        return []


def get_all_robdef_plugin_factories() -> List[PyriRobDefPluginFactory]:
    robdefs = dict()
    all_eps = entry_points()
    if "pyri.plugins.robdef" not in all_eps:
        return []

    ret = []
    eps = all_eps["pyri.plugins.robdef"]
    for ep in eps:
        factory_furc = ep.load()
        ret.append(factory_furc)
    return ret

def get_all_plugin_robdefs() -> Dict[str,str]:
    robdefs = dict()
    all_eps = entry_points()
    if "pyri.plugins.robdef" not in all_eps:
        return dict()

    eps = all_eps["pyri.plugins.robdef"]
    for ep in eps:
        ep_func = ep.load()
        plugin_robdefs = ep_func().get_robdefs()
        for robdef in plugin_robdefs:
            for l in robdef.splitlines():
                l = l.strip()
                if l.startswith('#'):
                    continue
                robdef_name_match = re.match('^service[ \t]+((?:[a-zA-Z](?:\\w*[a-zA-Z0-9])?)(?:\\.[a-zA-Z](?:\\w*[a-zA-Z0-9])?)+)$', l)
                if robdef_name_match is None:
                    warnings.warn(f'Invalid robdef starting with: {l}')
                    break
                robdef_name = robdef_name_match.group(1)
                if robdef_name not in robdefs:
                    robdefs[robdef_name] = robdef
                break

    return robdefs

def register_all_plugin_robdefs(node: "RobotRaconteur.RobotRaconteurNode") -> None:
    robdefs_dict = get_all_plugin_robdefs()
    if len(robdefs_dict) > 0:
        robdefs = list(robdefs_dict.values())
        node.RegisterServiceTypes(robdefs)
    