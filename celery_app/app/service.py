from app.exceptions import ServiceError
from time import sleep


def add(x, y):
    try:
        sleep(3)
        result = x + y
        return result
    except ServiceError:
        raise
