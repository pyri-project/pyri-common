from importlib.metadata import entry_points
from typing import List, Any

def get_plugin_factories(plugin_type: str) -> List[Any]:
    all_eps = entry_points()
    if plugin_type not in all_eps:
        return []

    ret = []
    eps = all_eps[plugin_type]
    for ep in eps:
        factory_func = ep.load()
        ret.append(factory_func())
    return ret