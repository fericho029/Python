summa = int(input("Введите сумму: "))

kolvo_100 = summa // 100
summa %= 100

kolvo_50 = summa // 50
summa %= 50

kolvo_10 = summa // 10
summa %= 10

kolvo_5 = summa // 5
summa %= 5

kolvo_2 = summa // 2
summa %= 2

kolvo_1 = summa

print("\n100 руб:", kolvo_100)
print("50 руб:", kolvo_50)
print("10 руб:", kolvo_10)
print("5 руб:", kolvo_5)
print("2 руб:", kolvo_2)
print("1 руб:", kolvo_1)
