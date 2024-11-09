import numpy as np


def get_matrix(shape):
    matrix = np.zeros(shape, dtype=np.int8)

    matrix[0::2, 1::2] = 1
    matrix[1::2, 0::2] = 1

    return matrix


if __name__ == "__main__":
    print("Работа с библиотекой NumPy. Задача 1", end="\n\n")

    matrix = get_matrix(shape=(8, 8))
    print("Получена матрица:")
    print(matrix)

    np.savetxt(
        "./Module2/Lesson12/NumPy_task1_matrix.txt", matrix, fmt="%d", delimiter=" "
    )
    print("Матрица сохранена!")
