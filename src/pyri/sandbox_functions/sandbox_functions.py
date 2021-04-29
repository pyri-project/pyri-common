from pyri.plugins.sandbox_functions import PyriSandboxFunctionsPluginFactory
from pyri.sandbox_context import PyriSandboxContext
import numpy as np
import time

import general_robotics_toolbox as rox

from RobotRaconteurCompanion.Util.GeometryUtil import GeometryUtil

def time_wait(seconds):
    time.sleep(seconds)

def linalg_vector(string_vector):
    return np.fromstring(string_vector,sep=",").tolist()

def global_variable_get(global_name):

    device_manager = PyriSandboxContext.device_manager
    var_storage = device_manager.get_device_client("variable_storage", 1)    
    return var_storage.getf_variable_value("globals",global_name).data

def _convert_to_pose(a):
    # TODO: Convert named pose, transform, etc to pose
    if hasattr(a, "pose"):
        if hasattr(a.pose, "pose"):
            return a.pose.pose
        return a.pose
    return a

def geometry_pose_new(x,y,z,r_r,r_p,r_y):
    xyz = np.array([x,y,z],dtype=np.float64)
    rpy = np.deg2rad(np.array([r_r,r_p,r_y],dtype=np.float64))

    geom_util = GeometryUtil(node = PyriSandboxContext.node)

    return geom_util.xyz_rpy_to_pose(xyz,rpy)    

def geometry_pose_component_get(pose, component_name):
    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    xyz,rpy = geom_util.pose_to_xyz_rpy(_convert_to_pose(pose))
    rpy = np.rad2deg(rpy)

    if component_name == "X":
        return xyz[0]
    if component_name == "Y":
        return xyz[1]
    if component_name == "Z":
        return xyz[2]
    if component_name == "R_R":
        return rpy[0]
    if component_name == "R_P":
        return rpy[1]
    if component_name == "R_Y":
        return rpy[2]
    assert False, "Invalid pose component"

def geometry_pose_component_set(pose, component_name, value):
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
    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    T_a = geom_util.pose_to_rox_transform(_convert_to_pose(pose_a))
    T_b = geom_util.pose_to_rox_transform(_convert_to_pose(pose_b))
    T_res = T_a * T_b
    return geom_util.rox_transform_to_pose(T_res)

def geometry_pose_inv(pose):
    geom_util = GeometryUtil(node = PyriSandboxContext.node)
    T_rox = geom_util.pose_to_rox_transform(_convert_to_pose(pose))
    T_res = T_rox.inv()
    return geom_util.rox_transform_to_pose(T_res)

def _get_sandbox_functions():
    return {
        "time_wait": time_wait,
        "linalg_vector": linalg_vector,
        "global_variable_get": global_variable_get,
        "geometry_pose_new": geometry_pose_new,
        "geometry_pose_component_get": geometry_pose_component_get,
        "geometry_pose_component_set": geometry_pose_component_set,
        "geometry_pose_multiply": geometry_pose_multiply,
        "geometry_pose_inv": geometry_pose_inv
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