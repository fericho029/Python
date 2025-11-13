import datetime

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time = datetime.datetime.now().strftime("%H:%M:%S")
            name = func.__name__
            with open(filename, "a", encoding="utf-8") as f:
                f.write(f"[{time}] Функция: {name}, аргументы: {args} и {kwargs}\n")
            return func(*args, **kwargs)
        return wrapper
    return decorator


@log_calls("Logs.txt")
def summ(a, b):
    return a + b


summ(5, 3)
print(summ(9, 1))
