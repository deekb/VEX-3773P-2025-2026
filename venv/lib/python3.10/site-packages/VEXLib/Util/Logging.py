import time


def logged(func):
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        print(f"[{time.monotonic()} {func.__name__}]: args={args}, kwargs={kwargs}")
        output = func(*args, **kwargs)
        end_time = time.monotonic()
        print(f"[{time.monotonic()} {func.__name__}] {output}")
        print(f"[{time.monotonic()} {func.__name__}] {end_time-start_time}s")
        return output

    return wrapper


@logged
def hello(name):
    print(f"Hello {name}")


hello("Derek")
