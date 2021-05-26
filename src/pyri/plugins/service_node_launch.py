from typing import NamedTuple, List, Callable, Dict, Tuple
import argparse
import warnings
from . import util as plugin_util

def add_argument_warn(arg_parser: argparse.ArgumentParser, *args, **kwargs):
    try:
        arg_parser.add_argument(*args,**kwargs)
    except argparse.ArgumentError as e:
        if "conflicting option string" in e.message:
            warnings.warn(str(e))
        else:
            raise

def add_argument_silent(arg_parser: argparse.ArgumentParser, *args, **kwargs):
    try:
        arg_parser.add_argument(*args,**kwargs)
    except argparse.ArgumentError as e:
        if "conflicting option string" in e.message:
            #warnings.warn(str(e))
            pass
        else:
            raise

def _default_add_args(arg_parser):
    add_argument_silent(arg_parser, '--device-manager-url', type=str, default=None,required=False,help="Robot Raconteur URL for device manager service")
    add_argument_silent(arg_parser, '--device-manager-identifier', type=str, default=None,required=False,help="Robot Raconteur identifier for device manager service")
             
def _default_prepare_args(arg_results):
    args = []
    if arg_results.device_manager_url is not None:
        args.append(f"--device-manager-url={arg_results.device_manager_url}")
    if arg_results.variable_storage_identifier is not None:
        args.append(f"--device-manager-identifier={arg_results.device_manager_identifier}")
    return args

class ServiceNodeLaunch(NamedTuple):
    name: str
    plugin_name: str
    module_main: str
    add_arg_parser_options: Callable[[argparse.ArgumentParser],None] = _default_add_args
    prepare_service_args: Callable[[argparse.Namespace],List[str]] = _default_prepare_args
    depends: List[str] = ["device_manager"]
    depends_backoff: float = 1
    restart: bool = False
    restart_backoff: float = 5
    default_devices: List[Tuple[str,str]] = []
    extra_params: dict = None



class PyriServiceNodeLaunchFactory:
    def __init__(self):
        pass

    def get_plugin_name(self):
        return ""

    def get_service_node_launch_names(self) -> List[str]:
        return []

    def get_service_node_launches(self) -> List[ServiceNodeLaunch]:
        return []

def get_all_service_node_launch_plugin_factories() -> List[PyriServiceNodeLaunchFactory]:
    return plugin_util.get_plugin_factories("pyri.plugins.service_node_launch")

def get_all_service_node_launches() -> Dict[str,List[ServiceNodeLaunch]]:
    launches = dict()
    factories = get_all_service_node_launch_plugin_factories()

    for factory in factories:
        launches[factory.get_plugin_name()] = factory.get_service_node_launches()

    return launches
