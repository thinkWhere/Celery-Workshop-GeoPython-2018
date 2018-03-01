from celery_app import app
from time import sleep


@app.task
def add(x, y):
    """
    Simple task which adds two numbers
    :param x: integer
    :param y: integer
    :return: result of x + y
    """
    sleep(3)
    result = x + y
    return result
