from pyri.plugins.sandbox_functions import PyriSandboxFunctionsPluginFactory
from pyri.sandbox_context import PyriSandboxContext
import numpy as np
import time
import copy
import RobotRaconteur as RR

import general_robotics_toolbox as rox

from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil
import re

def util_copy(var):
    """
    Copy a local variable value

    Parameters:

    * var (Any): Variable to copy
    """

    # TODO: Restrict which objects can be copied?
    return copy.deepcopy(var)

def time_wait_for_completion(local_device_name, timeout):
    """
    Wait for an asynchronous operation to complete for specified
    device. Raises an error if timeout expires before completion.

    Parameters:

    * local_device_name (str): Name of the device to wait for completion
    * timeout (float): Wait timeout in seconds
    """
    PyriSandboxContext.action_runner.wait_for_completion(local_device_name, timeout)

def time_wait_for_completion_all(timeout):
    """
    Wait for all asynchronous operations on all devices to complete.
    Raises an error if timeout expires before completion.

    Parameters:

    * timeout (float): Wait timeout in seconds

    """
    PyriSandboxContext.action_runner.wait_for_completion_all(timeout)

def time_wait(seconds):
    """
    Wait for a specified time in seconds.
    
    Parameters:

    * seconds (float) Time to wait in seconds
    
    """
    time.sleep(seconds)

def linalg_vector(string_vector):
    """
    Create a new vector from a formatted string.

    Parameters:

    * string_vector (str): Vector in string format
    """
    return np.fromstring(string_vector,sep=",").tolist()

def global_variable_get(global_name):
    """
    Get the value of a global variable from the global variable table.

    Parameters:

    * global_name (str): The name of the global variable

    Return (Any): The value of the variable.
    """

    device_manager = PyriSandboxContext.device_manager
    var_storage = device_manager.get_device_client("variable_storage", 1)
    v = var_storage.getf_variable_value("globals",global_name).data
    if not isinstance(v, np.ndarray):
        return v
    var_info = var_storage.getf_variable_info("globals",global_name)
    var_type = RR.TypeDefinition()
    var_type.FromString(var_info.datatype)
    if var_type.ArrayType == RR.DataTypes_ArrayTypes_none:
        if issubclass(v.dtype.type,np.floating):
            return float(v[0])
        elif issubclass(v.dtype.type,np.integer):
            return int(v[0])
        return v[0]
    return v
    

def global_variable_set(global_name, value):
    """
    Set the value of a global variable in the global variable table. Global
    variable must already exist, and the specified value must be compatible
    with the global variable type.

    Parameters:

    * global_name (str): The name of the global variable
    * value (Any): The new value of the global variable
    """

    device_manager = PyriSandboxContext.device_manager
    var_storage = device_manager.get_device_client("variable_storage", 1)    
    var_info = var_storage.getf_variable_info("globals",global_name)
    var_type = var_info.datatype

    var_value = RR.VarValue(value,var_type)
    var_storage.setf_variable_value("globals", global_name, var_value)

def global_variable_add(global_name, datatype, value, persistence, reset_value):
    """
    Adds a new variable to the global variable table. The variable must not
    already exist.

    Parameters:

    * global_name (str): The name of the new global variable. Must match regex `^[a-zA-Z](?:\\w*[a-zA-Z0-9])?$`.
    * datatype (str): The type of the new variable. May be `number`, `array`, `matrix`, `string`, or
      a valid Robot Raconteur data type.
    * value (Any): The new variable value
    * persistence (str): The persistence of the new variable. May be `normal`, `temporary`,
      `persistent`, or `constant`.
    * reset_value (Any): The reset value of the variable. May be `None` for no value.
    """

    m = re.match("^[a-zA-Z](?:\\w*[a-zA-Z0-9])?$", global_name)
    assert m, f"Global name \"{global_name}\" is invalid"

    datatype = datatype.lower()
    if datatype == "number":
        rr_datatype = "double"
    elif datatype == "array":
        rr_datatype = "double[]"
    elif datatype == "matrix":
        rr_datatype = "double[*]"
    elif datatype == "string":
        rr_datatype = "string"
    else:
        assert False, f"Invalid type for new global variable: {datatype}"

    device_manager = PyriSandboxContext.device_manager
    node = PyriSandboxContext.node
    var_storage = device_manager.get_device_client("variable_storage", 1)

    var_consts = node.GetConstants('tech.pyri.variable_storage', var_storage)
    variable_persistence = var_consts["VariablePersistence"]
    variable_protection_level = var_consts["VariableProtectionLevel"]

    pers = persistence.lower()
    if pers == "normal":
        rr_pers = variable_persistence["normal"]
    elif pers == "temporary":
        rr_pers = variable_persistence["temporary"]
    elif pers == "persistent":
        rr_pers = variable_persistence["persistent"]
    elif pers == "constant":
        rr_pers = variable_persistence["constant"]
    else:
        assert False, f"Invalid persistence for new global variable: {pers}"

    var_storage.add_variable2("globals", global_name, rr_datatype, RR.VarValue(value, rr_datatype),
        [],{},rr_pers,RR.VarValue(reset_value,rr_datatype), variable_protection_level["read_write"], [], "User created variable", False)

def global_variable_delete(global_name):
    """
    Deletes a global variable

    Parameters:

    * global_name (str): The name of the global variable to delete
    """

    device_manager = PyriSandboxContext.device_manager
    var_storage = device_manager.get_device_client("variable_storage", 1)    

    var_storage.delete_variable("globals", global_name)

def _convert_to_pose(a):
    # TODO: Convert named pose, transform, etc to pose
    if hasattr(a, "pose"):
        if hasattr(a.pose, "pose"):
            return a.pose.pose
        return a.pose
    return a

def geometry_pose_new(x,y,z,r_r,r_p,r_y):
    """
    Create a new pose using XYZ-RPY format. Units are meters and degrees

    Parameters:

    * x (float): X position in meters
    * y (float): Y position in meters
    * z (float): Z position in meters
    * r_r (float): Roll in degrees
    * r_p (float): Pitch in degrees
    * r_y (float): Yaw in degrees

    Return (Pose): Pose named array
    """


    xyz = np.array([x,y,z],dtype=np.float64)
    rpy = np.deg2rad(np.array([r_r,r_p,r_y],dtype=np.float64))

    geom_util = GeometryUtil(node = PyriSandboxContext.node)

    return geom_util.xyz_rpy_to_pose(xyz,rpy)    

def geometry_pose_component_get(pose, component_name):
    """
    Get an XYZ-RPY component of a pose.

    Parameters:

    * pose (Pose): The pose
    * component_name (str): The component to get. May be `X`, `Y`, `Z`, `R_R`, `R_P`, or `R_Y`

    Return (float): The pose value
    """

    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    xyz,rpy = geom_util.pose_to_xyz_rpy(_convert_to_pose(pose))
    rpy = np.rad2deg(rpy)

    if component_name == "X":
        return float(xyz[0])
    if component_name == "Y":
        return float(xyz[1])
    if component_name == "Z":
        return float(xyz[2])
    if component_name == "R_R":
        return float(rpy[0])
    if component_name == "R_P":
        return float(rpy[1])
    if component_name == "R_Y":
        return float(rpy[2])
    assert False, "Invalid pose component"

def geometry_pose_component_set(pose, component_name, value):
    """
    Set an XYZ-RPY component of a pose. This function does not modify in place.
    It returns a new pose.

    Parameters:

    * pose (Pose): The pose
    * component_name (str): The component to get. May be `X`, `Y`, `Z`, `R_R`, `R_P`, or `R_Y`
    * value (float): The new pose component value in meters or degrees

    Return (Pose): The new pose with updated value

    """
    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    xyz,rpy = geom_util.pose_to_xyz_rpy(_convert_to_pose(pose))
    rpy = np.rad2deg(rpy)

    if component_name == "X":
        xyz[0] = value
    elif component_name == "Y":
        xyz[1] = value
    elif component_name == "Z":
        xyz[2] = value
    elif component_name == "R_R":
        rpy[0] = value
    elif component_name == "R_P":
        rpy[1] = value
    elif component_name == "R_Y":
        rpy[2] = value
    else:
        assert False, "Invalid pose component"

    rpy = np.deg2rad(rpy)
    return geom_util.xyz_rpy_to_pose(xyz,rpy)

def geometry_pose_multiply(pose_a, pose_b):
    """
    Multiply one pose with another

    Parameters:

    * pose_a (Pose): The first pose
    * pose_b (Pose): The second pose

    Return (Pose): The result of the multiplication
    """


    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    T_a = geom_util.pose_to_rox_transform(_convert_to_pose(pose_a))
    T_b = geom_util.pose_to_rox_transform(_convert_to_pose(pose_b))
    T_res = T_a * T_b
    return geom_util.rox_transform_to_pose(T_res)

def geometry_pose_inv(pose):
    """
    Invert a pose

    Parameters:

    pose (Pose): The pose to invert

    Return (Pose): The inverted pose
    """
    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    T_rox = geom_util.pose_to_rox_transform(_convert_to_pose(pose))
    T_res = T_rox.inv()
    return geom_util.rox_transform_to_pose(T_res)

def proc_result_get():
    """
    Return the current procedure result. This result is used
    by the main program state machine to determine the next step.

    Return (str): The current result. Default is `DEFAULT`
    """


    return PyriSandboxContext.proc_result

def proc_result_set(result):
    """
    Set the current procedure result. This result is used
    by the main program state machine to determine the next step.

    Parameters:

    * result (str): The new procedure result
    """

    PyriSandboxContext.proc_result = result
    

def _get_sandbox_functions():
    return {
        "time_wait": time_wait,
        "time_wait_for_completion": time_wait_for_completion,
        "time_wait_for_completion_all": time_wait_for_completion_all,
        "linalg_vector": linalg_vector,
        "global_variable_get": global_variable_get,
        "global_variable_set": global_variable_set,
        "global_variable_add": global_variable_add,
        "global_variable_delete": global_variable_delete,
        "geometry_pose_new": geometry_pose_new,
        "geometry_pose_component_get": geometry_pose_component_get,
        "geometry_pose_component_set": geometry_pose_component_set,
        "geometry_pose_multiply": geometry_pose_multiply,
        "geometry_pose_inv": geometry_pose_inv,
        "proc_result_get": proc_result_get,
        "proc_result_set": proc_result_set
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