"""Lesson20 Task5: Implementation of sorted function"""

from functools import partial


def sort_users_by_age(data, descending=False):
    """
    Sort a list of user dictionaries by their age
    """
    return sorted(data, key=lambda x: x["age"], reverse=descending)


# Ascending sort function
sort_users_by_age_ascending = partial(sort_users_by_age, descending=False)
# Descending sort function
sort_users_by_age_descending = partial(sort_users_by_age, descending=True)
