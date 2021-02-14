
from typing import List, Dict, TYPE_CHECKING
from importlib.metadata import entry_points
import re
import warnings
from . import util as plugin_util

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
    return plugin_util.get_plugin_factories("pyri.plugins.robdef")

def get_all_plugin_robdefs() -> Dict[str,str]:
    robdefs = dict()
    factories = get_all_robdef_plugin_factories()

    for factory in factories:        
        plugin_robdefs = factory.get_robdefs()
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
    