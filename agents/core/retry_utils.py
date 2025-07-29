import time
import functools
import logging

logger = logging.getLogger(__name__)

def retry_on_exception(
    max_retries=3,
    initial_delay=1.0,
    backoff_factor=2.0,
    exceptions=(Exception,)
):
    """
    Retry decorator with exponential backoff.

    :param max_retries: Number of retry attempts.
    :param initial_delay: Delay before first retry.
    :param backoff_factor: Multiplier for delay increase.
    :param exceptions: Tuple of exception types to retry on.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(
                        f"[Retry {attempt + 1}/{max_retries}] {func.__name__} failed: {e}"
                    )
                    if attempt == max_retries - 1:
                        raise
                    time.sleep(delay)
                    delay *= backoff_factor
        return wrapper
    return decorator
