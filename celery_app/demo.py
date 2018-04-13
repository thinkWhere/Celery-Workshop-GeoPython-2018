from app.tasks import do_task
import random


def call_do_task():
    """TODO - Challenge 1

    write a loop that will iterate 2500 times. Inside the loop, use the two helper functions get_random_x and
    get_random_y to get suitable x and y values, add these values to the queue.  You will need to use the special
    celery delay function to do this."""


def get_random_x():
    return random.randint(0, 700000)


def get_random_y():
    return random.randint(0, 1300000)


if __name__ == '__main__':

    call_do_task()
