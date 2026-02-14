candidates = {name: rate for name, rate in [
    ("Alex", 100)
]}

def log_to_file(file):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            args_str = ", ".join(map(str, args)) if args else ""
            kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items()) if kwargs else ""

            with open(file, "a", encoding="utf-8") as f:
                f.write(
                    f"Функция: {func.__name__}\n"
                    f"Аргументы: {args_str}\n"
                    f"Именованные аргументы: {kwargs_str}\n"
                    f"Результат:\n{result}\n"
                )
            return result
        return wrapper
    return decorator


@log_to_file("log.txt")
def add_candidate(name, rate):
    candidates[name] = rate
    return f"Кандидат {name} добавлен с рейтингом {rate}\n"

@log_to_file("log.txt")
def delete_candidate(name):
    del candidates[name]
    return f"Кандидат {name} удалён\n"

@log_to_file("log.txt")
def update_rating(name, rate):
    candidates[name] = rate
    return f"Рейтинг кандидата {name} изменён на {rate}\n"

@log_to_file("log.txt")
def check_candidates(candidates):
    formatted = "\n".join(f"{name}: {rate}" for name, rate in candidates.items())
    print(f"Кандидаты:\n{formatted}\n")
    return f"{formatted}\n"


# При старте очищаем файл
with open("log.txt", "w", encoding="utf-8") as f:
    f.write("Новый файл\n\n")

while True:
    value = int(input('''Выберите цифру от 0 до 4:
          0: Выйти
          1: Добавить кандидата
          2: Удалить кандидата
          3: Изменить рейтинг кандидата
          4: Просмотреть кандидатов\n'''))

    match value:
        case 0:
            break
        case 1:
            name = input("Введите имя нового кандидата: ")
            rate = int(input("Введите рейтинг нового кандидата: "))
            print(add_candidate(name, rate))
        case 2:
            name = input("Введите имя кандидата: ")
            print(delete_candidate(name))
        case 3:
            name = input("Введите имя кандидата: ")
            rate = int(input("Введите новый рейтинг кандидата: "))
            print(update_rating(name, rate))
        case 4:
            check_candidates(candidates)
