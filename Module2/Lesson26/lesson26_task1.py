"""
Lesson26 Task1: Implementation of a decorator 
that restricts access to a function based on user role.
"""

import functools

USER = {"role": None}


def role_required(role):
    """
    Decorator restricts access to a function based on user role.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if USER["role"] == role:
                return func(*args, **kwargs)
            return "Permission denied"

        return wrapper

    return decorator
