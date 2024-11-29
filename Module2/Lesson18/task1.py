"""Lesson18 Task1: Implementation of input checker function"""


def input_checker():
    """Function for checking input sequence of symbols"""
    data_input = input("Введите список значений через пробел: ")
    data_input = data_input.split()
    data = []

    for item in data_input:
        try:
            if "." in item:
                data.append(float(item))
            else:
                data.append(int(item))
        except ValueError:
            data.append(item)

    flag_any = any(isinstance(item, (int, float)) and item > 0 for item in data)
    flag_all = all(isinstance(item, (int, float)) for item in data)

    if flag_any:
        print("Список содержит хотя бы одно положительное число.")
    else:
        print("Список не содержит ни одного положительного числа.")

    if flag_all:
        print("Все элементы списка являются числами.")
        return sorted(data)

    print("Список содержит нечисловые значения.")
    return data
