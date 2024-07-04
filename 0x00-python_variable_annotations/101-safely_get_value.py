#!/usr/bin/env python3
"""Adding type annotations to function"""
from typing import TypeVar, Union, Any, Mapping, Sequence

T = TypeVar('T')


def safely_get_value(dct: Mapping, key: Any,
                     default: Union[T, None] = None) -> Union[Any, T]:
    """Get value from dict safely."""
    if key in dct:
        return dct[key]
    else:
        return default
