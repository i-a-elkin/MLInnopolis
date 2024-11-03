def task2():
    print("Задача2. Счастливый билет")

    ticket = input("Введите номер билета: ")

    if len(ticket) != 6:
        raise ValueError("Некорректное количество цифр в номере билета!")
    if not ticket.isnumeric():
        raise TypeError("Номер билета должен содержать только цифры!")

    if sum(map(int, ticket[:3])) == sum(map(int, ticket[-3:])):
        print("Счастливый")
    else:
        print("Обычный")


if __name__ == "__main__":
    task2()
