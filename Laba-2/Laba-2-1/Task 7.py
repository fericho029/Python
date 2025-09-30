str_input = sorted(input("Введите строку: "))
compressed = ""
count = 1

for i in range(1, len(str_input)):
    if str_input[i] == str_input[i - 1]:
        count += 1
    else:
        compressed += str_input[i - 1] + str(count)
        count = 1
compressed += str_input[len(str_input) - 1] + str(count)

print(f"Сжатая строка: {compressed}")
