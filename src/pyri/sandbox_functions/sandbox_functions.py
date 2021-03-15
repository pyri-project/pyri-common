from pyri.plugins.sandbox_functions import PyriSandboxFunctionsPluginFactory
from pyri.sandbox_context import PyriSandboxContext
import numpy as np
import time

def time_wait(seconds):
    time.sleep(seconds)

def linalg_vector(string_vector):
    return np.fromstring(string_vector,sep=",").tolist()

def _get_sandbox_functions():
    return {
        "time_wait": time_wait,
        "linalg_vector": linalg_vector
    }

class PyriCommonSandboxFunctionsPluginFactory(PyriSandboxFunctionsPluginFactory):
    def get_plugin_name(self):
        return "pyri-common"

    def get_sandbox_function_names(self):
        return list(_get_sandbox_functions().keys())

    def get_sandbox_functions(self):
        return _get_sandbox_functions()


def get_sandbox_functions_factory():
    return PyriCommonSandboxFunctionsPluginFactory()