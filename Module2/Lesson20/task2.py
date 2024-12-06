"""Lesson20 Task2: Implementation of nested functions"""


def get_list():
    """
    Get the input sequence of integers, separated by spaces, and returns
    the sequence as a list of integers
    """
    data = input("Введите последовательность целых чисел через пробел: ").split()
    if any("." in item for item in data):
        raise ValueError("Последовательность должна содержать только целые числа")

    try:
        return list(map(int, data))
    except ValueError as e:
        raise ValueError(
            "Последовательность должна содержать только целые числа"
        ) from e


def sort_func(func):
    """
    Takes a function that returns a list, and returns a sorted version of that list
    """
    return sorted(func())
