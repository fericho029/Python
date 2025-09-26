text = input("Введите строку:");
letters = "aeiouAEIOU";

result = ''.join(char for char in text if char not in letters);
print(f"Исходный текст: {text} ""\n"f"Итоговый текст: {result}");