from typing import Callable, List, Dict
from importlib.metadata import entry_points

class PyriSandboxFunctionsPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self):
        return ""

    def get_sandbox_function_names(self) -> List[str]:
        return []

    def get_sandbox_functions(self) -> Dict[str,Callable]:
        return {}

def get_sandbox_functions_plugin_factories() -> List[PyriSandboxFunctionsPluginFactory]:
    
    all_eps = entry_points()
    if "pyri.plugins.sandbox_functions" not in all_eps:
        return []

    ret = []
    eps = all_eps["pyri.plugins.sandbox_functions"]
    for ep in eps:
        factory_furc = ep.load()
        ret.append(factory_furc)
    return ret

def get_all_plugin_sandbox_functions() -> Dict[str,Callable]:

    ret = dict()

    all_eps = entry_points()
    if "pyri.plugins.sandbox_functions" not in all_eps:
        return []
    
    eps = all_eps["pyri.plugins.sandbox_functions"]
    for ep in eps:
        factory_furc = ep.load()
        ret.update(factory_furc().get_sandbox_functions())        
    return ret