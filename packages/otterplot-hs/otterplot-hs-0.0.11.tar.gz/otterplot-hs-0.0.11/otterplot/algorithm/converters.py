r"""
This module contains a few converting functions as utilities for the library.
"""
from typing import Union


def string_to_slice(slicestr: str) -> Union[slice, int]:
    r"""
    Converts a string representation of a slice in an actual slice. For example useful for the definitions of GridSpec

    Args:
        slicestr(str): a string representing a slice. E.g. 1:, :-1,2:3,4

    Returns:
        the slice representation. E.g: slice(1,None),slice(None,-1),slice(2,3),slice(4)
    """
    if slicestr == ':':
        return slice(None, None)
    else:
        if ':' in slicestr:
            parts = slicestr.split(':')
            for (idx, p) in enumerate(parts):
                if p == '':
                    parts[idx] = None
                else:
                    parts[idx] = int(p)
            if len(parts) == 2:
                return slice(parts[0], parts[1])
            elif len(parts) == 3:
                return slice(parts[0], parts[1], parts[2])
            else:
                raise ValueError('not a valid slice representation')
        else:
            try:
                return int(slicestr)
            except ValueError:
                raise ValueError('Cannot convert input string into single integer while converting slice')
