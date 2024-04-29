def get_core_utils() -> dict[str, callable]:
    """ Returns the core utility functions. """
    return {
        "map_func_to_list": _map_func_to_list,
        "get_val_from_dict": _get_val_from_dict,
    }

def _map_func_to_list(func: callable, lst: list[any]) -> list[any]:
    """ Maps a function to a list. """
    return [func(item) for item in lst]

def _get_val_from_dict(key: str, dictionary: dict[str, any]) -> any:
    """ Gets a value from a dictionary. """
    return dictionary[key]