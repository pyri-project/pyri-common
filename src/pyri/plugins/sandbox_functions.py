from typing import Callable, List, Dict
from . import util as plugin_util

class PyriSandboxFunctionsPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self) -> str:
        return ""

    def get_sandbox_function_names(self) -> List[str]:
        return []

    def get_sandbox_functions(self) -> Dict[str,Callable]:
        return {}

def get_sandbox_functions_plugin_factories() -> List[PyriSandboxFunctionsPluginFactory]:
    return plugin_util.get_plugin_factories("pyri.plugins.sandbox_functions")
    
def get_all_plugin_sandbox_functions() -> Dict[str,Callable]:

    ret = dict()
    factories = get_sandbox_functions_plugin_factories()        
    for factory in factories:        
        ret.update(factory.get_sandbox_functions())        
    return ret