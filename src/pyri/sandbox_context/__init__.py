import threading

class PyriSandboxContext(threading.local):
    node = None
    device_manager = None
    print_func = None

class PyriSandboxContextScope:
    def __init__(self, node, device_manager,print_func):
        self._node = node
        self._device_manager = device_manager
        self._print_func = print_func

    def __enter__(self):
        PyriSandboxContext.node = self._node
        PyriSandboxContext.device_manager = self._device_manager
        PyriSandboxContext.print_func = self._print_func

    def __exit__(self, type_, value, traceback):
        PyriSandboxContext.node = None
        PyriSandboxContext.device_manager = None
        PyriSandboxContext.print_func = None