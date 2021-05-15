import threading
import RobotRaconteur as RR
import time

class PyriSandboxContext(threading.local):
    node = None
    device_manager = None
    print_func = None
    action_runner = None
    context_vars = dict()
    proc_result = None

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
        PyriSandboxContext.proc_result = None

    def __exit__(self, type_, value, traceback):
        PyriSandboxContext.node = None
        PyriSandboxContext.device_manager = None
        PyriSandboxContext.print_func = None
        PyriSandboxContext.action_runner = None
        PyriSandboxContext.context_vars = dict()
        PyriSandboxContext.proc_result = None

class PyriSandboxActionRunner:

    def __init__(self):
        self.lock = threading.RLock()
        self._runners = dict()
        self._abort = False

    def run_action(self, local_device_name, gen, wait = False):
        with self.lock:
            if self._abort:
                raise RR.OperationAbortedException("Procedure has been aborted")
            current_r = self._runners.get(local_device_name,None)
            if current_r is not None:
                if current_r.running:
                    raise RR.InvalidOperationException(f"Device {local_device_name} already running action")
            r = PyriSandboxActionRunnerInst(self,local_device_name,gen,wait)
            self._runners[local_device_name] = r
            r.run()

    def _run_complete(self, local_device_name, err):
        #TODO: Stop all on errors?
        with self.lock:
            del self._runners[local_device_name]

    def wait_for_completion(self, local_device_name, timeout):
        with self.lock:
            d = self._runners.get(local_device_name, None)
            if d is None:
                return
        d.wait_for_completion(timeout)

    def wait_for_completion_all(self, timeout):        
        with self.lock:
            runners = list(self._runners.values())

        t_start = time.time()
        for r in runners:
            t_remaining = (t_start + timeout) - time.time()
            if t_remaining < 0:
                raise RR.OperationTimeoutException("Timeout waiting for all actions to finish")
            r.wait_for_completion(t_remaining)

    def abort(self):
        with self.lock:
            self._abort = True
            for v in self._runners.values():
                v.abort()



class PyriSandboxActionRunnerInst:
    def __init__(self, parent, local_device_name, gen, wait):
        self._parent = parent        
        self._gen = gen
        self._wait = wait
        self.running = True
        self.local_device_name = local_device_name
        self.error = None
        self.evt = threading.Event()

    def run(self):
        try:
            with self._parent.lock:
                self.running=True
            if self._wait is False:
                self._gen.AsyncNext(None, self._async_next_handler)
                return

            while True:
                try:
                    # TODO: Watch for motion verification requests
                    self._gen.Next()
                except RR.StopIterationException:
                    break
        except Exception as e:
            with self._parent.lock:
                self._done(e)
                raise
        else:
            with self._parent.lock:
                self._done(None)

    def _async_next_handler(self, state, err):
        with self._parent.lock:
            if not self.running:
                return
            try:
                if err:
                    self._done(err)
                if self._parent._abort:
                    self._done(RR.OperationAbortedException("Operation aborted"))
                    try:
                        self._gen.AsyncAbort(lambda e: None)
                    except Exception:
                        pass
                # TODO: Show user verification before Next?
                self._gen.AsyncNext(None, self._async_next_handler)
            except Exception as e:
                self._done(e)


    def _done(self, err):
        if err is not None:
            if not isinstance(err,RR.StopIterationException):
                self.error = err
        self.running = False
        self._parent._run_complete(self.local_device_name,err)
        self.evt.set()

    def wait_for_completion(self, timeout = 15.0):
        if not self.evt.wait(timeout):
            raise RR.OperationTimeoutException(f"Wait for device {self.local_device_name} timed out")
        with self._parent.lock:
            if self.error is not None:
                raise self.error

    def abort(self):
        self.error = RR.OperationAbortedException("Procedure has been stopped")
        self.evt.set()
        try:
            self._gen.AsyncAbort(lambda e: None)
        except Exception:
            pass
