import RobotRaconteur as RR
import argparse

import RobotRaconteurCompanion as RRC
from pyri.device_manager_client import DeviceManagerClient
from RobotRaconteurCompanion.Util.InfoFileLoader import InfoFileLoader
from RobotRaconteurCompanion.Util.AttributesUtil import AttributesUtil
from RobotRaconteurCompanion.Util.RobotUtil import RobotUtil
from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil
from pyri.util.robotraconteur import add_default_ws_origins
from pyri.plugins import robdef as robdef_plugins

import importlib_resources
import io


PyriService_NodeSetup_Default_Flags = RR.RobotRaconteurNodeSetupFlags_SERVER_DEFAULT \
    | RR.RobotRaconteurNodeSetupFlags_TCP_TRANSPORT_IPV4_DISCOVERY
PyriService_NodeSetup_Default_AllowedOverride = RR.RobotRaconteurNodeSetupFlags_SERVER_DEFAULT_ALLOWED_OVERRIDE


class PyriServiceNodeSetup(RR.RobotRaconteurNodeSetup):
    def __init__(self, node_name, tcp_port, flags = PyriService_NodeSetup_Default_Flags, \
            allowed_overrides = PyriService_NodeSetup_Default_AllowedOverride, \
            node = None, argv = None, rr_config = None, \
            extra_service_defs = [], device_info_type = "com.robotraconteur.device.DeviceInfo", \
            device_info_arg = None, default_info = None, \
            arg_parser = None, wait_signal = None, \
            display_description="PyRI Generic Service",
            no_standard_robdef = False, no_device_manager = False,
            device_manager_autoconnect = True,
            register_plugin_robdef = False):

            # Initialize node setup superclass            
            super().__init__(node_name, tcp_port, flags, allowed_overrides, node, argv, rr_config)

            # If passed node is None, assume default node
            if node is None:
                node = RR.RobotRaconteurNode.s

            # Set up and parse arguments
            if arg_parser is None:
                arg_parser = argparse.ArgumentParser(description=display_description)
            if device_info_arg is None:
                arg_parser.add_argument("--device-info-file", type=argparse.FileType('r'),default=None,required=False,help="Info file for service")

            arg_parser.add_argument('--device-manager-url', type=str, default=None,required=False,help="Robot Raconteur URL for device manager service")
            arg_parser.add_argument('--device-manager-identifier', type=str, default=None,required=False,help="Robot Raconteur identifier for device manager service")
            arg_parser.add_argument("--wait-signal",action='store_const',const=True,default=False, help="wait for SIGTERM or SIGINT (Linux only)")
            arg_parser.add_argument("--pyri-webui-server-port",type=int,default=8000,help="The PyRI WebUI port for websocket origin (default 8000)")

            args, _ = arg_parser.parse_known_args()
            self._argparse_results = args

            if not no_standard_robdef:
                # Register standard service types
                RRC.RegisterStdRobDefServiceTypes(node)

            if register_plugin_robdef:
                # Register all plugin robdef if requested
                robdef_plugins.register_all_plugin_robdefs(node)

            # Register additional passed service types
            extra_defs = []
            for d in extra_service_defs:
                if isinstance(d,tuple):
                    packg,res = d
                    extra_defs.append(importlib_resources.read_text(packg,res))
                elif isinstance(d,io.TextIOBase):
                    extra_defs.append(d.read())
                else:
                    extra_defs.append(d)
            if len(extra_defs) > 0:
                node.RegisterServiceTypes(extra_defs)

            if device_info_arg is None:
                device_info_arg = "device-info-file"

            device_info_arg_res = getattr(args,device_info_arg.replace("-","_"))
            if device_info_arg_res is None:
                if isinstance(default_info,tuple):
                    info_packg,info_res = default_info
                    device_info_text = importlib_resources.read_text(info_packg,info_res)
                elif isinstance(d,io.TextIOBase):
                   device_info_text = default_info.read()
                else:
                    device_info_text = default_info
            else:
                with device_info_arg_res:
                    device_info_text = device_info_arg_res.read()

            info_loader = InfoFileLoader(node)
            any_device_info, device_ident_fd = info_loader.LoadInfoFileFromString(device_info_text, device_info_type, "device")
            if device_info_type == "com.robotraconteur.device.DeviceInfo":
                device_info = any_device_info
            else:
                device_info = any_device_info.device_info

            attributes_util = AttributesUtil(node)
            device_attributes = attributes_util.GetDefaultServiceAttributesFromDeviceInfo(device_info)

            add_default_ws_origins(self.tcp_transport,args.pyri_webui_server_port)

            if args.wait_signal:
                self._wait_signal = True
            elif wait_signal == True:
                self._wait_signal = True
            else:
                self._wait_signal = False

            if not no_device_manager:
                self._device_manager = DeviceManagerClient(device_manager_url = args.device_manager_url, device_manager_identifier=args.device_manager_identifier, \
                    node = node, autoconnect = device_manager_autoconnect)
            else:
                self._device_manager = None

            self._device_info = device_info
            self._any_device_info = any_device_info
            self._device_ident_fd = device_ident_fd
            self._device_attributes = device_attributes
            self.node = node

    @property
    def device_manager(self):
        return self._device_manager

    @property
    def device_info_struct(self):
        return self._device_info

    @property
    def info_struct(self):
        return self._any_device_info

    @property
    def argparse_results(self):
        return self._argparse_results

    def wait_exit(self):
        if self._wait_signal:
            #Wait for shutdown signal if running in service mode
            print("Press Ctrl-C to quit...")
            import signal
            signal.sigwait([signal.SIGTERM,signal.SIGINT])
        else:
            #Wait for the user to shutdown the service            
            input("Server started, press enter to quit...")

    def register_service(self, service_name, service_obj_type, service_obj):
        ctx = self.node.RegisterService(service_name, service_obj_type, service_obj)
        ctx.SetServiceAttributes(self._device_attributes)
        return ctx
            