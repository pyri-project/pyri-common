import RobotRaconteur as RR
import threading
import traceback
import urllib.parse
import re
import ipaddress

from RobotRaconteurCompanion.Util.RobustFunctionCaller import RobustPollingAsyncFunctionCaller

class DeviceManagerClient:
    def __init__(self,device_manager_url: str, node: RR.RobotRaconteurNode = None, autoconnect = True, tcp_ipv4_only = False):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node

        self._active_devices=dict()
        self._autoconnect = autoconnect
        self._tcp_ipv4_only = tcp_ipv4_only

        self._device_added=RR.EventHook()
        self._device_removed=RR.EventHook()
        self._device_updated=RR.EventHook()

        self._device_manager = self._node.SubscribeService(device_manager_url)
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
        dev_res, dev_client = self._device_manager.TryGetDefaultClient()
        if not dev_res:
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
            pass
            #traceback.print_exc()

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
            for a in active_devices:
                if a.local_device_name not in self._active_devices:                    
                    if self._autoconnect:
                        urls = self._filter_urls(a.urls)
                        if len(urls) == 0:
                            continue
                        a_client = self._node.SubscribeService()
                        self._active_devices[a.local_device_name] = (a,a_client)
                        try:
                            self._device_added.fire(a.local_device_name)
                        except:
                            traceback.print_exc()
                    else:
                        self._active_devices[a.local_device_name] = (a,None)
            a_names = [a.local_device_name for a in active_devices]
            for a in list(self._active_devices.keys()):
                if a not in a_names:
                    a_client = self._active_devices[a][1]
                    del self._active_devices[a]
                    if a_client is not None:
                        try:
                            a_client.Close()
                        except: pass
                    try:
                        self._device_removed.fire(a)
                    except:
                        traceback.print_exc()


    def get_device_names(self):
        with self._lock:
            return self._active_devices.keys()

    def get_device_info(self, local_device_name):
        with self._lock:
            return self._active_devices[local_device_name][0]

    def get_device_client(self, local_device_name,timeout = 0):
        with self._lock:
            sub = self._active_devices[local_device_name][1]
            if not self._autoconnect and sub is None:
                assert False, "Device not connected"                
        return sub.GetDefaultClientWait(timeout)

    def get_device_subscription(self, local_device_name):
        with self._lock:
            sub = self._active_devices[local_device_name][1]
            if not self._autoconnect and sub is None:
                assert False, "Device not connected"
            return sub

    def connect_device(self, local_device_name):
        with self._lock:
            a = self._active_devices.get(local_device_name)
            assert a is not None, f"Invalid device requested: {local_device_name}"
            a=a[0]
            urls = self._filter_urls(a.urls)
            if len(urls) > 0:
                a_client = self._node.SubscribeService(urls)
            else:
                a_client = None
            self._active_devices[local_device_name] = (a,a_client)

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
