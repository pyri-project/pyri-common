import threading
import RobotRaconteur as RR

class PyriSandboxContext(threading.local):
    node = None
    device_manager = None
    print_func = None
    action_runner = None
    context_vars = dict()

class PyriSandboxContextScope:
    def __init__(self, node, device_manager,print_func, action_runner):
        self._node = node
        self._device_manager = device_manager
        self._print_func = print_func
        self._action_runner = action_runner

    def __enter__(self):
        PyriSandboxContext.node = self._node
        PyriSandboxContext.device_manager = self._device_manager
        PyriSandboxContext.print_func = self._print_func
        PyriSandboxContext.action_runner = self._action_runner
        PyriSandboxContext.context_vars = dict()

    def __exit__(self, type_, value, traceback):
        PyriSandboxContext.node = None
        PyriSandboxContext.device_manager = None
        PyriSandboxContext.print_func = None
        PyriSandboxContext.action_runner = None
        PyriSandboxContext.context_vars = dict()

class PyriSandboxActionRunner:
    def run_action(self, local_device_name, gen, wait = False):
        if wait is False:
            raise NotImplemented("Asynchronous action wait not implemented")

        while True:
            try:
                # TODO: Watch for motion verification requests
                gen.Next()
            except RR.StopIterationException:
                break