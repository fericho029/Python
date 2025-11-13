def type_check(expected_type):
    def decorator(func):
        def wrapper(arg):
            if not isinstance(arg, expected_type):
                raise TypeError(
                    f"Ошибка: функция '{func.__name__}' ожидает аргумент типа {expected_type.__name__}, "
                    f"но получен {type(arg).__name__} ({arg!r})"
                )
            return func(arg)
        return wrapper
    return decorator


@type_check(int)
def square(x):
    return x * x


print(square(5))
print(square("5"))