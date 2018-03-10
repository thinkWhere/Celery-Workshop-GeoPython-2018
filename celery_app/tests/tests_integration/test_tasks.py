from app.tasks import add_task
import pytest

previous_num = 0


def test_add(celery_worker):

    assert add_task.delay(4, 4).get(timeout=5) == 8

#
# def test_call_tasks(celery_session_worker):
#     """Make x number of asynchronous task executions."""
#     global previous_num
#     iterations = 20
#
#     for num in range(iterations):
#
#         result = add_task.delay(num, previous_num)
#         previous_num = num
#
#         assert result.get() == num + previous_num
#         print(f"called add({num}, {previous_num})")
