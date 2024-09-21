import time
from functools import wraps


def retry(times=3, delay=1, exceptions=(Exception,)):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attemps = 0
            
            while attemps < times:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attemps += 1
                    if attemps >= times:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator