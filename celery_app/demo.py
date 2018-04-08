from app.tasks import gridify_task
import random

iterations = 1000


def call_gridify_task():
    """Call the gridify task x times."""
    global iterations
    x_max = 700000
    y_max = 1300000

    for task_execution in range(iterations):

        x = random.randint(0, x_max)
        y = random.randint(0, y_max)

        gridify_task.delay(x, y)

        print(f"called gridify({x}, {y}) asynchronously")


if __name__ == '__main__':

    call_gridify_task()
