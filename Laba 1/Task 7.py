sek = int(input("Введите количество секунд: "))

min = sek // 60
sek %= 60

print(min, "минута(ы) ",sek," секунда(ы)")  
