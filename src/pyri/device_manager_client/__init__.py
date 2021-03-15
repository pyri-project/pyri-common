import RobotRaconteur as RR
import threading
import traceback

class DeviceManagerClient:
    def __init__(self,device_manager_url: str, node: RR.RobotRaconteurNode = None, autoconnect = True):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node

        self._active_devices=dict()
        self._autoconnect = autoconnect

        self._device_manager = self._node.SubscribeService(device_manager_url)

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

    def _refresh_devices2(self,active_devices):
        with self._lock:            
            for a in active_devices:
                if a.local_device_name not in self._active_devices:                    
                    if self._autoconnect:
                        a_client = self._node.SubscribeService(a.urls)
                        self._active_devices[a.local_device_name] = (a,a_client)
                    else:
                        self._active_devices[a.local_device_name] = (a,None)
            a_names = [a.local_device_name for a in active_devices]
            for a in list(self._active_devices.keys()):
                if a not in a_names:
                    del self._active_devices[a]

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
            a_client = self._node.SubscribeService(a.urls)
            self._active_devices[local_device_name] = (a,a_client)

    @property
    def device_manager(self):
        with self._lock:
            return self._device_manager
        

