#!/usr/bin/env python3
"""Defines 'wait_n' async routine"""
import asyncio
from typing import List
task_wait_random = __import__('3-tasks').wait_random


async def task_wait_n(n: int, max_delay: int) -> List[float]:
    """Executes 'wait_n' coroutine"""
    tasks = [task_wait_random(max_delay) for _ in range(n)]
    completed_tasks, _ = await asyncio.wait(tasks)
    sorted_delays = sorted(task.result() for task in completed_tasks)
    return sorted_delays
