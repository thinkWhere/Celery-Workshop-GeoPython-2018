from celery_app import app
from time import sleep
from celery import Task


class AppBaseTask(Task):
    """

    """
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print('{0!r} failed: {1!r}'.format(task_id, exc))


@app.task(base=AppBaseTask, bind=True)
def add(self, x, y):
    """Simple task which adds two numbers

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    :param x: integer
    :param y: integer
    @:returns result of x + y
    """
    sleep(3)
    result = x + y
    return result
