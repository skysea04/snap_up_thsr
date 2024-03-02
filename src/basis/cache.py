import time
from datetime import date
from functools import wraps

from .constants import Time


def expire_cache(seconds: int = Time.TEN_MINUTES, refresh_on_next_day: bool = False):
    def cache_decorator(func):
        cache_data = {}

        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = (args, frozenset(kwargs.items()))
            current_day = date.today()

            if cache_key in cache_data:
                result, timestamp, last_day = cache_data[cache_key]
                if refresh_on_next_day and (last_day is None or last_day != current_day):
                    pass  # Skip returning the cached result and refresh the cache
                elif time.time() - timestamp < seconds:
                    return result

            result = func(*args, **kwargs)
            cache_data[cache_key] = (result, time.time(), current_day)
            return result

        def clear(*args, **kwargs):
            cache_key = (args, frozenset(kwargs.items()))
            if cache_key in cache_data:
                del cache_data[cache_key]

        wrapper.clear = clear
        return wrapper

    return cache_decorator
