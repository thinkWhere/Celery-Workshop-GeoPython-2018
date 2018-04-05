from time import sleep

class ServiceError(Exception):
    """Custom exception for service errors"""
    pass


def add(x, y):
    """This function is called from the task.

    Notes:
        - Don't pass Database/ORM objects to tasks.

    Args:
        x: integer
        y: integer

    Returns: result of task

    """
    # TODO: Replace with geo related task
    try:
        sleep(3)
        result = x + y
        return result
    except ServiceError:
        raise
