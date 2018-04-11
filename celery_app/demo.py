from app.tasks import do_task
import random


def call_do_task():
    """Call the do_task task x times."""
    iterations = 1000000

    for task_execution in range(iterations):

        x = get_random_x()
        y = get_random_y()

        do_task.delay(x, y)

        print(f"called do_task({x}, {y}) asynchronously")


def get_random_x():
    return random.randint(0, 700000)


def get_random_y():
    return random.randint(0, 130000)


if __name__ == '__main__':

    call_do_task()
