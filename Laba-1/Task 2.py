text = input("Введите строку:");
letters = "aeiouAEIOU";

result = ''.join(char for char in text if char not in letters);
print(text, "\n", result);