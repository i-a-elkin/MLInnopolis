import numpy as np


def get_vectorn(len, mu=0, var=1, random_seed=None):
    np.random.seed(random_seed)

    return mu + (var**0.5) * np.random.randn(len)


if __name__ == "__main__":
    print("Работа с библиотекой NumPy. Задача 2", end="\n\n")

    vectorn = get_vectorn(2000, mu=0, var=5, random_seed=20)
    print(f"Среднее значение: {np.mean(vectorn):.3f}")
    print(f"Дисперсия: {np.var(vectorn):.3f}")
