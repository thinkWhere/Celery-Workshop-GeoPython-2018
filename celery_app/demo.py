from app.tasks import add_task
import random

iterations = 1000

def call_add_number_task():
    """Call the add task x times."""
    global iterations
    x_max = 700000
    y_max = 1300000

    for task_execution in range(iterations):

        x = random.randint(0, x_max)
        y = random.randint(0, y_max)

        add_task.delay(x, y)

        print(f"called add({x}, {y})")



if __name__ == '__main__':

    call_add_number_task()
