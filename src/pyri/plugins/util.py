from importlib.metadata import entry_points
from typing import List, Any

def get_plugin_factories(plugin_type: str) -> List[Any]:
    all_eps = entry_points()
    if hasattr(all_eps, "groups"):        
        if plugin_type not in all_eps.groups:
            return []
    else:
        if plugin_type not in all_eps:
            return []

    found_eps=set()
    ret = []
    if hasattr(all_eps, "select"):
        eps = all_eps.select(group=plugin_type)
    else:
        eps = all_eps[plugin_type]
    for ep in eps:
        if ep.name in found_eps:
            continue
        found_eps.add(ep.name)
        factory_func = ep.load()
        ret.append(factory_func())
    return ret