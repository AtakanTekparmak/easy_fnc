from typing import Union

def get_core_utils() -> dict[str, callable]:
    """ Returns the core utility functions. """
    return {
        "get_val_from_dict": _get_val_from_dict,
        "concatenate_strings": _concatenate_strings,
        "_mean": _mean,
    }

def _get_val_from_dict(key: str, dictionary: dict[str, any]) -> any:
    """ Gets a value from a dictionary. """
    return dictionary[key]

def _concatenate_strings(lst: list[str]) -> str:
    """ Concatenates a list of strings. """
    return "".join(lst)

def _mean(lst: list[Union[int, float]]) -> float:
    """ Calculates the mean of a list of numbers. """
    return sum(lst) / len(lst)