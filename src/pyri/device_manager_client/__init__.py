import RobotRaconteur as RR
import threading

class DeviceManagerClient:
    def __init__(self,device_manager_url: str, node: RR.RobotRaconteurNode = None):
        self._lock = threading.RLock()
        if node is None:
            self._node = RR.RobotRaconteurNode.s
        else:
            self._node = node

        self._active_devices=dict()

        self._device_manager = self._node.SubscribeService(device_manager_url)

    def refresh_devices(self, timeout = 0):
        dev_res, dev_client = self._device_manager.TryGetDefaultClientWait(timeout)
        if not dev_res:
            raise Exception("Could not connect to device manager")

        active_devices = dev_client.getf_active_devices()

        with self._lock:
            for a in active_devices:
                if a.local_device_name not in self._active_devices:
                    a_client = self._node.SubscribeService(a.urls)
                    self._active_devices[a.local_device_name] = (a,a_client)

    def get_device_names(self):
        with self._lock:
            return self._active_devices.keys()

    def get_device_info(self, local_device_name):
        with self._lock:
            return self._active_devices[local_device_name][0]

    def get_device_client(self, local_device_name,timeout = 0):
        with self._lock:
            sub = self._active_devices[local_device_name][1]
        return sub.GetDefaultClientWait(timeout)

    def get_device_subscription(self, local_device_name):
        with self._lock:
            return self._active_devices[local_device_name][1]
        

