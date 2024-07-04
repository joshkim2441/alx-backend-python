#!/usr/bin/env python3
"""Defines make_multiplier function."""
from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function that multiplies a float by multiplier."""
    def multiplier_function(x: float) -> float:
        """Multiplies a float by multiplier."""
        return x * multiplier
    return multiplier_function
