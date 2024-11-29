"""Lesson18 Task3: Implementation of password generator function"""

import random


def password_generator(population, password_len=12):
    """Function for random password generation"""
    while True:
        password = [random.choice(population) for _ in range(password_len)]
        yield "".join(password)
