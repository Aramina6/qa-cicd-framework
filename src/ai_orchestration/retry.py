import asyncio
import time
from functools import wraps
from typing import Callable, TypeVar, Awaitable

T = TypeVar("T")

class RetryConfig:
    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

def async_retry(config: RetryConfig):
    """Decorator for retrying async LLM calls with exponential backoff."""
    def decorator(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(config.max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:   # In real code you would catch specific errors (RateLimit, Timeout, etc.)
                    last_exception = e
                    if attempt == config.max_retries:
                        break
                    delay = min(config.base_delay * (2 ** attempt), config.max_delay)
                    await asyncio.sleep(delay)
            raise last_exception or RuntimeError("Retry failed")
        return wrapper
    return decorator
