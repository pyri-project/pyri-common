import RobotRaconteur as RR
import numpy as np

def _numpy_to_plain(d):
    return d.tolist()

def _varvalue_to_plain(d):
    return robotraconteur_data_to_plain(d.data)

def _struct_to_plain(d):
    ret = dict()
    fields = dir(d)
    for f in fields:
        if f.startswith("_"):
            continue
        if f.lower().startswith("rr"):
            continue
        ret[f] = robotraconteur_data_to_plain(getattr(d,f))

    return ret

def _list_to_plain(d):
    ret = []
    for d1 in d:
        ret.append(robotraconteur_data_to_plain(d1))
    return ret

def _dict_to_plain(d):
    ret = dict()
    for k,v in d.items():
        ret[k] = robotraconteur_data_to_plain(v)
    return ret

def robotraconteur_data_to_plain(d):
    if isinstance(d,RR.RobotRaconteurStructure):
        return _struct_to_plain(d)

    if isinstance(d,RR.VarValue):
        return _varvalue_to_plain(d)

    if isinstance(d,list):
        return _list_to_plain(d)

    if isinstance(d,dict):
        return _dict_to_plain(d)

    if isinstance(d,str):
        return d

    if isinstance(d,int):
        return d
    
    if isinstance(d,float):
        return d

    if isinstance(d,np.ndarray):
        return _numpy_to_plain(d)