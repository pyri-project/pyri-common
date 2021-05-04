import RobotRaconteur as RR
import numpy as np
import netifaces
import socket

def _numpy_to_plain(d):
    l = d.tolist()
    for i in range(len(l)):
        if isinstance(l[i],np.ndarray):
            l[i] = _numpy_to_plain(l[i])
    return l

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

def add_default_ws_origins(tcp_transport, port = -1, localhost=True, local_adapter_ips=True, hostname=True):

    if port == -1:
        port = tcp_transport.GetListenPort()

    if localhost:
        if port == 80:
            tcp_transport.AddWebSocketAllowedOrigin("http://localhost")
            tcp_transport.AddWebSocketAllowedOrigin("http://127.0.0.1")
        if port == 443:
            tcp_transport.AddWebSocketAllowedOrigin("https://localhost")
            tcp_transport.AddWebSocketAllowedOrigin("https://127.0.0.1")
        
        tcp_transport.AddWebSocketAllowedOrigin(f"http://localhost:{port}")
        tcp_transport.AddWebSocketAllowedOrigin(f"https://localhost:{port}")

        tcp_transport.AddWebSocketAllowedOrigin(f"http://127.0.0.1:{port}")
        tcp_transport.AddWebSocketAllowedOrigin(f"https://127.0.0.1:{port}")

    if hostname:

        h = socket.gethostname()

        if port == 80:
            tcp_transport.AddWebSocketAllowedOrigin(f"http://{h}")
        if port == 443:
            tcp_transport.AddWebSocketAllowedOrigin(f"https://{h}")
        
        tcp_transport.AddWebSocketAllowedOrigin(f"http://{h}:{port}")
        tcp_transport.AddWebSocketAllowedOrigin(f"https://{h}:{port}")

    if local_adapter_ips:

        inters = netifaces.interfaces()
        for inter in inters:
            addrs = netifaces.ifaddresses(inter)
            addrs2 = addrs.get(netifaces.AF_INET,[])
            for addr in addrs2:
                addr = addr["addr"]
                if addr == '127.0.0.1':
                    # Include localhost using the "localhost" option
                    continue
                
                if port == 80:
                    tcp_transport.AddWebSocketAllowedOrigin(f"http://{addr}")
                if port == 443:
                    tcp_transport.AddWebSocketAllowedOrigin(f"https://{addr}")
                
                tcp_transport.AddWebSocketAllowedOrigin(f"http://{addr}:{port}")
                tcp_transport.AddWebSocketAllowedOrigin(f"https://{addr}:{port}")
