from celery import Celery

app = Celery('tasks', broker='amqp://celery_user:secret@rabbitmq:5672/celery_app')
