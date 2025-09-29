str = input("Введите список чисел через пробел: ")
items = str.split()
numbers = []

for item in items:
    try:
        numbers.append(int(item))
    except:
        print("Ошибка")
        exit()

numbers_sorted = sorted(set(numbers), reverse=True)

# Проверка наличия второго элемента
if len(numbers_sorted) < 2:
    print("Недостаточно чисел")
else:
    print(f"Второе по величине число: {numbers_sorted[1]}")
