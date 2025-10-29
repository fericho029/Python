list_input = input("Введите список")
items = list_input.split()
unique_items = []

for item in items:
    if item not in unique_items:
        unique_items.append(item)

print(f"Список без дубликатов: {unique_items}")
