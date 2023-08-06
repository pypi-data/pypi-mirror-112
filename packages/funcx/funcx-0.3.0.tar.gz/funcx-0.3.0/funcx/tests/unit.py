from functools import wraps


def imported_fn(x):
    return x + 1


def decorator(func):
    def wrapper(*args, **kwargs):
        x = func(*args, **kwargs)
        return f"wrap {x} wrap"
    return wrapper


def decorator_2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        x = func(*args, **kwargs)
        return f"wrap2 {x} wrap2"
    return wrapper


@decorator
def imported_decorated_fn(x):
    return x


@decorator_2
def imported_decorated_fn_2(x):
    return x
