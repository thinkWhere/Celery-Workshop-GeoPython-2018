from celery import Celery

application = Celery('tasks', broker='amqp://celery_user:secret@rabbitmq:5672/celery_app')
