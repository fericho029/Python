str = input("Введите список чисел: ")
items = str.split()
numbers = []

for item in items:
    if item.isdigit():
        numbers.append(float(item))
    else:
        print("Неверный список")
        exit()

unique = sorted([x for x in numbers if numbers.count(x) == 1])
duplicates = sorted(list(set([x for x in numbers if numbers.count(x) > 1])))
chet = sorted([x for x in numbers if x.is_integer() and int(x) % 2 == 0])
nechet = sorted([x for x in numbers if x.is_integer() and int(x) % 2 != 0])
negative = sorted([x for x in numbers if x < 0])
floats = sorted([x for x in numbers if not x.is_integer()])
sum = sum([x for x in numbers if x.is_integer() and int(x) % 5 == 0])
max_num = max(numbers)
min_num = min(numbers)

print(f"1. Уникальные числа: {unique}")
print(f"2. Повторяющиеся числа: {duplicates}")
print(f"3. Четные числа: {chet} \nНечетные числа: {nechet}")
print(f"4. Отрицательные числа: {negative}")
print(f"5. Числа с плавающей точкой: {floats}")
print(f"6. Сумма чисел, кратных 5: {sum}")
print(f"7. Самое большое число: {max_num}")
print(f"8. Самое маленькое число: {min_num}")
