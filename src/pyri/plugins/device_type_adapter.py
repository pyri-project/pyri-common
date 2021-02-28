from typing import List, Dict, Any, NamedTuple
from . import util as plugin_util

class PyriDeviceTypeAdapterExtendedState(NamedTuple):
    robotraconteur_type: str
    display_flags: List[str]
    state_data: Any


class PyriDeviceTypeAdapter:
    def __init__(self, device_subscription):
        pass

    def get_robotraconteur_type(self) -> str:
        pass

    async def get_extended_device_infos(self, timeout = 0) -> Dict[str,"RobotRaconteur.VarValue"]:
        pass

    async def get_extended_device_states(self, timeout = 0) -> Dict[str,PyriDeviceTypeAdapterExtendedState]:
        pass

class PyriDeviceTypeAdapterPluginFactory:
    def __init__(self):
        super().__init__()

    def get_plugin_name(self) -> str:
        return ""

    def get_robotraconteur_types(self) -> List[str]:
        return []

    def create_device_type_adapter(self, robotraconteur_type: str, client_subscription: Any) -> PyriDeviceTypeAdapter:
        return None

def get_device_type_adapter_plugin_factories() -> List[PyriDeviceTypeAdapterPluginFactory]:
    return plugin_util.get_plugin_factories("pyri.plugins.device_type_adapter")
    
def get_all_robotraconteur_types() -> List[str]:

    ret = []
    factories = get_device_type_adapter_plugin_factories()        
    for factory in factories:        
        ret.extend(factory.get_robotraconteur_types())        
    return ret

def create_device_type_adapter(robotraconteur_type: str, client_subscription: Any) -> PyriDeviceTypeAdapter:
    factories = get_device_type_adapter_plugin_factories()

    for f in factories:
        rr_types = f.get_robotraconteur_types()
        if robotraconteur_type in rr_types:
            return f.create_device_type_adapter(str, client_subscription)
    
    assert False, "Invalid robotraconteur_type device type adapter requested"