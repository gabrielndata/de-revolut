from collections import defaultdict


def traverse_dict(_dict: dict):
    """Traverse nested dictionary"""

    for key, value in _dict.items():
        yield key
        if type(value) in (dict, defaultdict):
            yield from traverse_dict(value)
        else:
            yield value


def traverse_to_hashable(_dict: dict):
    for i in traverse_dict(_dict):
        yield tuple(map(tupleit, i))


def tupleit(item):
    """Convert object to tuple"""
    if isinstance(item, list):
        return tuple(map(tupleit, item))
    elif isinstance(item, dict):
        t = []
        for k, v in item.items():
            t.append((k, *map(tupleit, tupleit(v))) if isinstance(v, (list, dict)) else (k, v))
        return tuple(t)
    return item
