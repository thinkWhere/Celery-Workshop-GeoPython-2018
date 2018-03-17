from time import sleep


class ServiceError(Exception):
    """Custom exception for service errors"""
    pass


def add(x, y):
    try:
        sleep(3)
        result = x + y
        return result
    except ServiceError:
        raise
