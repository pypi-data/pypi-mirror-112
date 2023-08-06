from typing import Callable



def silent(function: Callable, *args, **kwargs):
    try:
        callable(*args, **kwargs)
    except Exception:
        pass


async def async_silent(function: Callable, *args, **kwargs):
    try:
        await callable(*args, **kwargs)
    except Exception:
        pass