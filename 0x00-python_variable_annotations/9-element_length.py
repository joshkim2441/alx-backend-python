#!/usr/bin/env python3
"""Annotate function element_length."""
from typing import Sequence, Iterable, List, Tuple


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Annotate function element_length."""
    return [(i, len(i)) for i in lst]
