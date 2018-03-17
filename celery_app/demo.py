from app.tasks import add_task


iterations = 30


def call_tasks():
    global iterations

    for task_execution in range(iterations):

        other_num = 3 + iterations
        add_task.delay(iterations, other_num)

        print(f"called add({iterations}, {other_num})")
        iterations = other_num


if __name__ == '__main__':
    call_tasks()
