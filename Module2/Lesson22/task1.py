"""Lesson22 Task1: Implementation of multi-threaded function."""

import time
from ast import literal_eval
from concurrent.futures import ThreadPoolExecutor, as_completed


def process_number(number, delay=0.2):
    """
    Processes a given number by doubling its value after a specified delay.
    """
    time.sleep(delay)
    return number * 2


def process_data(data, num_workers=10):
    """
    Processes a list of numerical lists concurrently and
    computes their processing time and sum of processed results.
    """
    logs = {"time": [], "sum": []}
    futures = [[] for _ in range(len(data))]

    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        for i, lst in enumerate(data):
            start_time = time.time()
            for number in lst:
                future = executor.submit(process_number, number)
                futures[i].append(future)

            logs["sum"].append(
                sum(future.result() for future in as_completed(futures[i]))
            )
            logs["time"].append(time.time() - start_time)

    return logs


if __name__ == "__main__":
    with open("./test_list_numbers.txt", encoding="utf-8") as file:
        DATA = "".join([line.strip() for line in file.readlines()])
        DATA = literal_eval(DATA)

    results = process_data(DATA)
    fastest_result = min(zip(results["time"], results["sum"]), key=lambda x: x[0])[1]

    # Результат может изменяться от запуска к запуску,
    # т.к. расчет значений имеет близкую скорость выполнения
    print(f"results['time']: {results['time']}")
    print(f"results['sum']: {results['sum']}")
    print(f"Сумма чисел в первом обработанном списке: {fastest_result}")
