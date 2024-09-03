import numpy as np
import asyncio


async def test():
    print("123")


def func():
    print("hello from func")

    asyncio.run(test())

    return np.array([1, 2, 3])
