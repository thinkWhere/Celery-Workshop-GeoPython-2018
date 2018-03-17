FROM python:3.6.4-alpine3.7

ADD . /celery_app

RUN pip install -r /celery_app/requirements.txt

WORKDIR /celery_app

CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
