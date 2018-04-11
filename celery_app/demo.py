from app.tasks import do_task
import random

iterations = 1


def call_do_task():
    """Call the do_task task x times."""
    global iterations
    x_max = 700000
    y_max = 1300000

    for task_execution in range(iterations):

        x = random.randint(0, x_max)
        y = random.randint(0, y_max)

        do_task.delay(x, y)

        print(f"called do_task({x}, {y}) asynchronously")


if __name__ == '__main__':

    call_do_task()
