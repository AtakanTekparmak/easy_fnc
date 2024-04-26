def _map_func_to_list(func: callable, lst: list[any]) -> list[any]:
    """ Maps a function to a list. """
    return [func(item) for item in lst]

def _get_val_from_dict(key: str, dictionary: dict[str, any]) -> any:
    """ Gets a value from a dictionary. """
    return dictionary[key]