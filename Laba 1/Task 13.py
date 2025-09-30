import random

secret = random.randint(1, 100)
guess = None

print("Я загадал число от 1 до 100. Попробуй угадать!")

while guess != secret:
    guess = int(input("Твоя догадка: "))
    
    if guess < secret:
        print("Больше!")
    elif guess > secret:
        print("Меньше!")
    else:
        print("Угадал!")
