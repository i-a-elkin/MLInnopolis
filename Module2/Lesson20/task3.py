"""Lesson20 Task3: Implementation of strings permutations function"""

from itertools import permutations


def get_permutations(data, n):
    """
    Generates all possible permutations of a given length from the input sequence
    and returns them in sorted order
    """
    return sorted(permutations(data, n))
