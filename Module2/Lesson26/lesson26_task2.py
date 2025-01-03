"""
Lesson26 Task2: Implementation of cache decorator.
"""

import functools
import numpy as np

CACHE = {}


def get_key_cache(db, expiration_time, thing):
    """
    Function generates key for cache database.
    """
    return f"db={db},expiration_time={expiration_time},thing={thing}"


def get_info(thing):
    """
    Function returns information about 'thing'.
    """
    return f"{thing} info: {np.random.randint(1, 10000)}"


def cache(db, expiration_time):
    """
    Decorator adds information about 'thing' and expire time to cache database
    and get information from it during expiration time.
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(thing):
            key_cache = get_key_cache(db, expiration_time, thing)
            if key_cache not in CACHE:
                CACHE[key_cache] = [get_info(thing), expiration_time]
                print(
                    f"Info about: {thing} from {db}, now cached with expire={
                        CACHE[key_cache][1]}"
                )
                CACHE[key_cache][1] -= 1
                return CACHE[key_cache][0]
            if CACHE[key_cache][1] > 0:
                print(
                    f"Info about: {thing} cached in {db}, expire={CACHE[key_cache][1]}"
                )
                CACHE[key_cache][1] -= 1
                return CACHE[key_cache][0]
            print(f"Info about: {thing} cached in {db}, expire={CACHE[key_cache][1]}")
            del CACHE[key_cache]
            return "Caсhe has been cleared!"

        return wrapper

    return decorator
