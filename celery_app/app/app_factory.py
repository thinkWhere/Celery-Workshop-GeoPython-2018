from celery import Celery


def create_app():
    """Create a Celery app instance.

    Returns: Celery app

    """
    application = Celery('tasks', broker='amqp://celery_user:secret@rabbitmq:5672/celery_app')
    return application
