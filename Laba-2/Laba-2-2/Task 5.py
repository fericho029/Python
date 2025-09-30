def cache(func):
    saved = {}
    def wrapper(*args):
        if args in saved:
            print("Кэш")
            return saved[args]
        print("Вычисляю")
        result = func(*args)
        saved[args] = result
        return result
    return wrapper

@cache
def multiply(a, b):
    return a * b

print(multiply(3, 4), "\n")
print(multiply(3, 4), "\n")
print(multiply(10, 4), "\n")
print(multiply(3, 4), "\n")