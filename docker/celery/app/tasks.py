from celery_app import app


@app.task
def add(x, y):
    """
    Simple task which adds two numbers
    :param x: integer
    :param y: integer
    :return: result of x + y
    """
    result = x + y
    return result
