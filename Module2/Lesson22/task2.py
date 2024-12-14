"""Lesson22 Task2: Implementation of multiprocessing function."""

import zipfile
import multiprocessing
import time


def get_number(file_name, path_to_archive_1, path_to_archive_2, counter, lock):
    """
    Retrieves a number from nested files within two zip archives.
    """
    with zipfile.ZipFile(path_to_archive_1, "r") as archive_1:
        with archive_1.open(file_name) as file:
            path_to_number = file.readline().decode("utf-8").strip().replace("\\", "/")

    with zipfile.ZipFile(path_to_archive_2, "r") as archive_2:
        with archive_2.open(path_to_number) as file:
            number = float(file.readline().decode("utf-8").strip())

    with lock:
        counter.value += number

    return number


def get_sum_numbers(path_to_archive_1, path_to_archive_2):
    """
    Computes the sum of numbers retrieved from nested files
    within two zip archives using multiprocessing.
    """
    manager = multiprocessing.Manager()
    counter = manager.Value("f", 0.0)
    lock = manager.Lock()

    with zipfile.ZipFile(path_to_archive_1, "r") as archive_1:
        files_names = [item for item in archive_1.namelist() if item.endswith(".txt")]

    with multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1) as pool:
        results = pool.starmap(
            get_number,
            [
                (file_name, path_to_archive_1, path_to_archive_2, counter, lock)
                for file_name in files_names
            ],
        )

    return sum(results), counter.value


if __name__ == "__main__":
    start_time = time.time()
    result = get_sum_numbers("./path_8_8.zip", "./recursive_challenge_8_8.zip")

    print(f"Сумма значений pool.starmap(): {result[0]}")
    print(f"Значение глобального счетчика: {result[1]}")
    print(f"Время выполнения программы: {int(time.time() - start_time)} сек")
