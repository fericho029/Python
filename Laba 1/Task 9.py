ip = input("Введите IP-адрес: ")

parts = ip.split(".")

if len(parts) == 4:
    check = True
    for part in parts:
        if not part.isdigit() or not (0 <= int(part) <= 255):
            check = False
            break
    if check:
        print("Корректный IP-адрес!")
    else:
        print("Некорректный IP-адрес.")
else:
    print("Некорректный IP-адрес.")
