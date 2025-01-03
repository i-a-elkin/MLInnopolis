"""
Lesson26 Task3: Implementation of context manager for safe writing.
"""

from contextlib import contextmanager


@contextmanager
def safe_write(file_name, mode="w", encoding="utf-8"):
    """
    A context manager for safe writing to a file with error handling and caching.
    """

    # Read the initial file data and save it to cache
    try:
        with open(file_name, mode="r", encoding=encoding) as file:
            initial_data_cache = file.read()
    except FileNotFoundError:
        initial_data_cache = ""

    # Write to the file and handle exceptions
    try:
        with open(file_name, mode=mode, encoding=encoding) as file:
            yield file
    except Exception as e:
        print(f"Во время записи в файл было возбуждено исключение {type(e).__name__}")
        with open(file_name, mode="w", encoding=encoding) as file:
            file.write(initial_data_cache)
