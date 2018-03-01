FROM python:3.6.4-alpine3.7

ADD . /celery_app

WORKDIR /celery_app

RUN pip install -r requirements.txt

WORKDIR /celery_app/app

CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
