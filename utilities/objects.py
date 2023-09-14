from functools import reduce
from dict_deep import deep_set, deep_get


def has_property(d, path):
    try:
        reduce(lambda x, y: x[y], path.split("."), d)
        return True
    except KeyError:
        return False


# Throwing in this approach for nested get for the heck of it...
def _get_property(d, path, *default):
    try:
        return reduce(lambda x, y: x[y], path.split("."), d)
    except KeyError:
        if default:
            return default[0]
        raise


def get_property(source: any, path: str) -> any:
    return deep_get(source, path)


def set_property(target: any, path: str, value: any) -> None:
    """
    An altered version of 'deep_set' of the "dict_deep" library to intercept dot notation property paths to allow the
    paths to contain indexed lists.
    """
    if '.[' in path and '].' in path:
        left_path = path.split('.[', 1)
        left_index = left_path[1][:1]
        right_path = path.split('].', 1)
        right_index = right_path[0][-1]
        index = int(left_index)

        if int(left_index) != int(right_index):
            index = int(left_index + '' + right_index)

        temp_list = deep_get(target, left_path[0])

        if temp_list is None:
            temp_list = [{}]

        elif len(temp_list) < index + 1:
            temp_list.append({})

        temp_list_item = temp_list[index]
        set_property(temp_list_item, right_path[1], value)
        deep_set(target, left_path[0], temp_list)
    else:
        deep_set(target, path, value)
