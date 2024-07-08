#!/usr/bin/env python3
"""Returns an asyncio.Task from an integer"""

import asyncio
from typing import Any

wait_random = __import__('0-basic_async_syntax').wait_random

def task_wait_random(max_delay: int) -> Any:
    """
    Creates an asyncio.Task for wait_random with specified max_delay
    Returns an asyncio.Task from an integer
    """
    return asyncio.create_task(wait_random(max_delay))
