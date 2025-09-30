import time

def timing(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        ms = (end - start) * 1000
        print(f"Время выполнения: {ms:.2f} мс")
        return result
    return wrapper


@timing
def slow_function():
    time.sleep(0.5)
    return 0


print(slow_function())