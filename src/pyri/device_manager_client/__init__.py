from pathlib import Path
import RobotRaconteur as RR
import threading
import traceback
import urllib.parse
import re
import ipaddress
import uuid

from RobotRaconteurCompanion.Util.RobustFunctionCaller import RobustPollingAsyncFunctionCaller
try:
    import RobotRaconteurCompanion.Util.LocalIdentifiersManager as local_ident_manager
except:
    pass

from RobotRaconteurCompanion.Util.DeviceConnector import DeviceConnector, DeviceConnectorDetails


class DeviceManagerClient:
    def __init__(self,device_manager_url: str = None, device_manager_identifier = None, node: RR.RobotRaconteurNode = None, autoconnect = True, tcp_ipv4_only = False):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node

        self._connect_request_devices = set()
        self._connect_request_device_types = set()

        self._active_device_specs = {}
        self._autoconnect = autoconnect
        self._device_connector = DeviceConnector(node=self._node, autoconnect=autoconnect)
        self._tcp_ipv4_only = tcp_ipv4_only

        self._device_added=RR.EventHook()
        self._device_removed=RR.EventHook()
        self._device_updated=RR.EventHook()
        if device_manager_url is not None:
            self._device_manager = self._node.SubscribeService(device_manager_url)
        else:
            if device_manager_identifier is None:
                device_manager_identifier = "pyri_device_manager"
            filter = _DeviceManagerConnectFilter(self._node, device_manager_identifier)
            self._device_manager = self._node.SubscribeServiceByType("tech.pyri.device_manager.DeviceManager", filter.get_filter())
        
        self._device_manager.ClientConnected += self._device_manager_client_connected

        self._poller = RobustPollingAsyncFunctionCaller(self._update_poll_f, (), error_handler=self._poller_err_handler, poll_interval=25, node=self._node)
        self._poller.poll_data += self._refresh_devices2

    def _update_poll_f(self, h, t):
        dev_client = self._device_manager.GetDefaultClient()                    
        dev_client.async_getf_active_devices(h, t)

    def _poller_err_handler(self, err):
        # TODO: Pass error information
        pass

    def _device_manager_client_connected(self, sub, subscription_id, c):
        c.device_added += self._device_added_evt
        c.device_removed += self._device_removed_evt
        c.device_updated += self._device_updated_evt

        self._evt_refresh_devices()

    def _device_added_evt(self, device, local_device_name):
        self._evt_refresh_devices()

    def _device_removed_evt(self, local_device_name):
        self._evt_refresh_devices()

    def _device_updated_evt(self, local_device_name):
        self._evt_refresh_devices()

    def _evt_refresh_devices(self):
        self._poller.request_poll()
            
    async def async_refresh_devices(self, timeout = 0):
        try:
           dev_client = await self._device_manager.AsyncGetDefaultClient(None, timeout)
        except Exception:
            raise Exception("Could not connect to device manager")

        # TODO: Add timeout arg
        active_devices = await dev_client.async_getf_active_devices(None)

        self._refresh_devices2(active_devices)

    def refresh_devices(self, timeout = 0):
        try:
            dev_res, dev_client = self._device_manager.TryGetDefaultClientWait(timeout)
            if not dev_res:
                raise Exception("Could not connect to device manager")

            active_devices = dev_client.getf_active_devices()

            self._refresh_devices2(active_devices)
        except:
            
            traceback.print_exc()

    def _filter_urls(self,urls):
        if not self._tcp_ipv4_only:
            return urls
        
        ret = []

        for u in urls:
            u1 = urllib.parse.urlparse(u)

            if re.match(r"^rrs?\+tcp$",u1.scheme) is not None \
                or re.match(r"^rrs?\+wss?$",u1.scheme) is not None:
                
                netloc = u1.netloc
                netloc_re = re.match(r"^(.*?)(\:\d+)?$",netloc)
                if netloc_re is None:
                    ret.append(u)
                    continue

                netloc = netloc_re.group(1)

                try:
                    netloc = netloc.strip("[]")
                    ipaddr = ipaddress.ip_address(netloc)
                except ValueError:
                    # Assume a hostname?
                    ret.append(u)
                else:
                    if isinstance(ipaddr,ipaddress.IPv4Address):
                        ret.append(u)

        return ret


    def _refresh_devices2(self,active_devices):
        with self._lock:
            current_devices = list(self._device_connector.DeviceNicknames)
            self._active_device_specs = {a.local_device_name: a for a in active_devices}       
            for a in active_devices:
                if a.local_device_name not in current_devices:                   
                    enabled =  self._autoconnect or a.local_device_name in self._connect_request_devices or \
                        a.root_object_type in self._connect_request_device_types or \
                        not self._connect_request_device_types.isdisjoint(a.root_object_implements)

                    urls = self._filter_urls(a.urls)
                    if len(urls) == 0:
                        enabled = False
                    a_name = a.local_device_name
                    print(f"Adding device {a_name} with urls {urls}")
                    a_details = DeviceConnectorDetails(device_nickname=a_name, urls=urls)
                    self._device_connector.AddDevice(a_details, force_connect=enabled)
                    
                    self._node.PostToThreadPool(lambda a_name=a_name: self._device_added.fire(a_name))
                        
            a_names = [a.local_device_name for a in active_devices]
            for a in list(self._device_connector.DeviceNicknames):
                if a not in a_names:
                    self._device_connector.RemoveDevice(a)
                    
                    self._node.PostToThreadPool(lambda a=a: self._device_removed.fire(a))
                    


    def get_device_names(self):
        with self._lock:
            return self._device_connector.DeviceNicknames

    def get_device_info(self, local_device_name):
        with self._lock:
            return self._active_device_specs[local_device_name]

    def get_device_client(self, local_device_name,timeout = 0,force_create=False):
        with self._lock:
            sub = self._device_connector.GetDevice(local_device_name, force_create=force_create)             
        return sub.GetDefaultClientWait(timeout)

    def get_device_subscription(self, local_device_name, force_create=False):
        with self._lock:
            return self._device_connector.GetDevice(local_device_name, force_create=force_create)

    def connect_device(self, local_device_name):
        with self._lock:
            self._device_connector.ConnectDevice(local_device_name)
                    

    def connect_device_type(self, device_type):
        with self._lock:
            self._connect_request_device_types.add(device_type)
            for a in self._active_device_specs.values():
                if a.root_object_type not in self._connect_request_device_types \
                    and self._connect_request_device_types.isdisjoint(a.root_object_implements):
                    continue
                self._device_connector.ConnectDevice(a.local_device_name)

    @property
    def device_manager(self):
        with self._lock:
            return self._device_manager

    @property
    def device_added(self):
        return self._device_added
    @device_added.setter
    def device_added(self,value):
        assert value == self._device_added
        
    @property
    def device_removed(self):
        return self._device_removed
    @device_removed.setter
    def device_removed(self,value):
        assert value == self._device_removed

    @property
    def device_updated(self):
        return self._device_updated
    @device_updated.setter
    def device_updated(self,value):
        assert value == self._device_updated

    def close(self):
        self._poller.close()

class _DeviceManagerConnectFilter:
    def __init__(self,node,  device_manager_identifier):
        self._node = node
        ident_str, ident_uuid = _parse_identifier(device_manager_identifier)

        assert ident_str is not None, "Invalid device manager identifier specified"

        if ident_uuid is None:
            try:
                node_dirs = self._node.GetNodeDirectories()
                device_ident_dir = Path(str(node_dirs.user_config_dir)).joinpath("identifiers").joinpath("device")
                device_ident_file = device_ident_dir.joinpath(ident_str)
                if device_ident_file.is_file():
                    with open(device_ident_file) as f:
                        ident_data = f.read()
                    ident_uuid = uuid.UUID(ident_data)                
            except:
                traceback.print_exc()
                pass
        self.ident_str = ident_str
        self.ident_uuid = ident_uuid

    def get_filter(self):
        ret = RR.ServiceSubscriptionFilter()
        ret.MaxConnections = 10
        ret.Predicate = self._predicate

        return ret

    def _predicate(self, service_info2):
        try:
            d_ident = service_info2.Attributes.get("device",None)
            if not d_ident:
                return False
            d_ident_n, d_ident_id = _parse_identifier(d_ident.data)
            if d_ident_n is None or d_ident_id is None:
                return False
            d_ident_id2 = uuid.UUID(d_ident_id)
            if self.ident_uuid is not None:
                return d_ident_n == self.ident_str and d_ident_id2 == self.ident_uuid
            else:
                return d_ident_n == self.ident_str
        except:
            traceback.print_exc()
        return False

def _parse_identifier(string_ident):
    
    name_regex_str = "(?:[a-zA-Z](?:[a-zA-Z0-9_]*[a-zA-Z0-9])?)(?:\\.[a-zA-Z](?:[a-zA-Z0-9_]*[a-zA-Z0-9])?)*"
    uuid_regex_str = "\\{?[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}\\}?"
    identifier_regex = "(?:(" + name_regex_str + ")\\|(" + uuid_regex_str + "))|(" + name_regex_str + ")|(" + uuid_regex_str + ")"

    r_res = re.match(identifier_regex, string_ident)
    if r_res is None:
        raise RR.InvalidArgumentException("Invalid identifier string")
    if r_res.group(1) is not None and r_res.group(2) is not None:
        return r_res.group(1), r_res.group(2)
    elif r_res.group(3) is not None:
        return r_res.group(3), None
    elif r_res.group(4) is not None:
        return r_res.group(4)

    assert False, "Internal error parsing device manager identifier"
