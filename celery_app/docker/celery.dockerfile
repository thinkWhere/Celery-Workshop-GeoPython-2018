FROM python:3.6.4-alpine3.7

COPY requirements/celery_app.txt /celery_app/requirements/celery_app.txt

RUN pip install --upgrade pip

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install -r /celery_app/requirements/celery_app.txt \
  && apk del build-deps

WORKDIR /celery_app

COPY . /celery_app

CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
