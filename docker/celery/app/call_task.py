from tasks import add

iterations = 20
previous_num = 1


def call_tasks():
    """
    Make x number of asynchronous task executions
    """
    for num in range(iterations):
        global previous_num

        add.delay(num, previous_num)
        previous_num = num
        print(f"called add({num}, {previous_num})")


if __name__ == '__main__':
    call_tasks()
