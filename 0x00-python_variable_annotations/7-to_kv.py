#!/usr/bin/env python3
"""Defines to_kv function."""
from typing import Union, Tuple


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    """Converts a float to a tuple of a string and a float."""
    return (k, v ** 2)
