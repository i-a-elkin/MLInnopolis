"""Lesson20 Task4: Implementation of symbols combinations function"""

from itertools import combinations


def get_combinations(data, n):
    """
    Generates all possible combinations of lenghts from 1 to n from the input
    sequence and returns them in sorted order
    """
    result = []
    for k in range(1, n + 1):
        result.extend(list(combinations(data, k)))

    return sorted(result, key=lambda x: (len(x), x))
