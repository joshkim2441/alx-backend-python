#!/usr/bin/env python3
"""Defines 'wait_n' async routine"""
import asyncio
from typing import List
wait_random = __import__('0-basic_async_syntax').wait_random


async def wait_n(n: int, max_delay: int) -> List[float]:
    """Executes 'wait_n' coroutine"""
    tasks = [wait_random(max_delay) for _ in range(n)]
    completed_tasks, _ = await asyncio.wait(tasks)
    sorted_delays = sorted(task.result() for task in completed_tasks)
    return sorted_delays
