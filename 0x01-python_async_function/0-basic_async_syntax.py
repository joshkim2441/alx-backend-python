#!/usr/bin/env python3
"""Defines a coroutine called async_comprehension."""

import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    """
    Waits for a random delay between 0 and max_delay
    Return the random float between 0 and max_delay.
    """
    delay = random.random() * max_delay
    await asyncio.sleep(delay)
    return delay
