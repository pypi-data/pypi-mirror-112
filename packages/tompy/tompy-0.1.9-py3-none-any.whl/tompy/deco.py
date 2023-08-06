import asyncio
from functools import wraps
from typing import Any, Awaitable, Callable


def sync(async_func: Callable[..., Awaitable[Any]]) -> Callable[..., Any]:
    @wraps(async_func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        return asyncio.run(async_func(*args, **kwargs))

    return wrapper
