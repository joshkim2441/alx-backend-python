#!/usr/bin/env python3
"""Using 'mymy' to validate code and apply changes"""
from typing import Tuple, List

def zoom_array(lst: List[int], factor: int = 2) -> List[int]:
    zoomed_in = [
        item for item in lst
        for _ in range(factor)
    ]
    return zoomed_in


array = [12, 72, 91]

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)

