"""Lesson20 Task1: Implementation of filter function"""


def is_len_ge(length):
    """
    Return a comparator function that checks if the length of an input is
    greater or equal than a specified length
    """

    def comparator(data):
        """
        Comparator function
        """
        if len(data) < length:
            return False
        return True

    return comparator
