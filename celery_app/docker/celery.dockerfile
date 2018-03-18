FROM python:3.6.4-alpine3.7

COPY . /celery_app

RUN pip install --upgrade pip

RUN pip install -r /celery_app/requirements/celery_app.txt

WORKDIR /celery_app

CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
