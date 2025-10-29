first_input = input("Введите первый список: ")
second_input = input("Введите второй список: ")

first_items = first_input.split()
second_items = second_input.split()

first_numbers = []
second_numbers = []

for item in first_items:
    try:
        first_numbers.append(int(item))
    except:
        print("Ошибка в первом списке")
        exit()

for item in second_items:
    try:
        second_numbers.append(int(item))
    except:
        print("Ошибка во втором списке")
        exit()

in_first_and_second = sorted([x for x in first_numbers if x in second_numbers])
only_in_first = sorted([x for x in first_numbers if x not in second_numbers])
only_in_second = sorted([x for x in second_numbers if x not in first_numbers])
combined = sorted(only_in_first + only_in_second)

print(f"\n1. Общие числа: {in_first_and_second}")
print(f"2. Только в первом списке: {only_in_first} \nТолько во втором списке: {only_in_second}")
print(f"3. Все, кроме общих: {combined}")
