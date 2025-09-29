password = input("Введите пароль");

if len(password) < 16:
    print("Слишком короткий")
elif password.isdigit() or password.isalpha():
    print("Слабый пароль")
else:
    print("Надежный пароль")    