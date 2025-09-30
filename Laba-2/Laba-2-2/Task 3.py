import datetime

def log_calls(filename):
    def decorator(func):
        def wrapper(*args, **kwargs):
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            name = func.__name__
            args_str = ", ".join(repr(a) for a in args)
            kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
            all_args = ", ".join(filter(None, [args_str, kwargs_str]))
            line = f"[{time}] {name}({all_args})\n"
            with open(filename, "a", encoding="utf-8") as f:
                f.write(line)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_calls("Logs.txt")
def summ(a,b):
    return a+b

summ(5,3)
print(summ(9,1))