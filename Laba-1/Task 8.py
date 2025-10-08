word = input("Введите слово: ").lower()

if word == word[::-1]:
    print("Это палиндром!")
else:
    print("Это не палиндром.")
