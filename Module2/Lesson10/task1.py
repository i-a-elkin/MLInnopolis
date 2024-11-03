def task1():
    print("Задача1. Максимум, минимум, остальное")
    
    nums = []
    messages = ["первое", "второе", "третье"]
    for i in range(3):
        num = input(f"Введите {messages[i]} число: ")
        nums.append(int(num))

    results = [max(nums), min(nums), sum(nums) - (max(nums) + min(nums))]
    messages = ["Максимум", "Минимум", "Остальное"]

    print(
        *[f"{message}: {result}" for result, message in zip(results, messages)],
        sep="\n",
    )


if __name__ == "__main__":
    task1()
