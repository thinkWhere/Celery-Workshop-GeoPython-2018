from celery import Task

from app.app_factory import create_app
from app.service import geoprocess, ServiceError

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
def do_task(self, x, y):
    # TODO: Update docstring
    """Performs simple geoprocessing task.

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

    # TODO - Challenge 2
    """
    The app.service.geoprocess artificially throws an artificial error to simulate a recoverable error.  Catch this
    error, and use celery's retry mechanism to retry processing the task.
    """
    try:
        geoprocess(x, y)
    except Exception as exc:
        raise TaskError(exc)
