import math
import types


def dict_to_namespace(root, depth = math.inf):

    if depth == 0:
        return root

    depth -= 1

    for (key, value) in root.items():
        if not isinstance(value, dict):
            continue
        root[key] = dict_to_namespace(value, depth = depth)

    return types.SimpleNamespace(**root)


def noop(*args, **kwargs):

    pass
