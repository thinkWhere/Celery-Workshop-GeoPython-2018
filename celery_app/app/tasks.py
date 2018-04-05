from app.service import gridify, ServiceError
from app.app_factory import create_app

from celery import Task


application = create_app()


class TaskError(Exception):
    """Custom exception for handling task errors"""
    pass


class AppBaseTask(Task):
    """Base Task

    The base Task class can be used to define
    shared behaviour between tasks.

    """

    abstract = True

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        # TODO: log out here
        super(AppBaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        # TODO: log out here
        super(AppBaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)


@application.task(base=AppBaseTask, bind=True, max_retries=3, soft_time_limit=5)
def add_task(self, x, y):
    """Simple task to adds two integers.

    Failed tasks are retried x times by the Task classes on_retry method.
    When tasks fail completely they are handled by the Task classes on_failure method

    Args:
        self: instance of the Task
        x: integer
        y: integer

    Raises:
        TaskError: failed tasked are handled by the parent task class.
    Returns:
        result of addition

    """
    try:
        result = gridify(x, y)
    except ServiceError as e:
        raise TaskError(e)
    except Exception as exc:
        self.retry(countdown=10, exc=exc)
