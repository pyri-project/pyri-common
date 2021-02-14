from typing import List, Dict, NamedTuple, TYPE_CHECKING
from importlib.metadata import entry_points
import re
import warnings

class PyriBlocklyCategory(NamedTuple):
    name: str
    json: str

class PyriBlocklyBlock(NamedTuple):
    name: str
    category: str
    doc: str
    json: str
    python_generator: str



class PyriBlocklyPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return ""

    def get_category_names(self) -> List[str]:
        return []

    def get_categories(self) -> List[PyriBlocklyCategory]:
        return []

    def get_block_names(self) -> List[str]:
        return []

    def get_block(self,name) -> PyriBlocklyBlock:
        return None

    def get_all_blocks(self) -> Dict[str,PyriBlocklyBlock]:
        return []

def get_all_robdef_blockly_factories() -> List[PyriBlocklyPluginFactory]:
    robdefs = dict()
    all_eps = entry_points()
    if "pyri.plugins.blockly" not in all_eps:
        return []

    ret = []
    eps = all_eps["pyri.plugins.blockly"]
    for ep in eps:
        factory_furc = ep.load()
        ret.append(factory_furc())
    return ret

def get_all_blockly_blocks() -> Dict[str,PyriBlocklyBlock]:
    factories = get_all_robdef_blockly_factories()
    ret = dict()
    for f in factories:
        ret.update(f.get_all_blocks())
    return ret