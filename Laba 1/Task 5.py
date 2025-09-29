number = int(input("Введите число: "))

if number % 7 == 0:
    print("Магическое число!")
else:
    summa = sum(int(x) for x in str(number))
    print("Сумма цифр:", summa)
