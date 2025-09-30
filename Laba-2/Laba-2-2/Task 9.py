def type_check(expected_type):
    def decorator(func):
        def wrapper(arg):
            if type(arg) != expected_type:
                raise TypeError("Неверный тип")
            return func(arg)
        return wrapper
    return decorator


@type_check(int)
def square(x):
    return x * x

print(square(5))     
print(square("5"))   
