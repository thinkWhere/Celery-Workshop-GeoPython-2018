FROM python:3.6.4-alpine3.7

COPY . /celery_app

RUN pip install --upgrade pip

RUN pip install -r /celery_app/requirements/flower_app.txt

RUN apk update \
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  && pip install psycopg2 \
  && apk del build-deps

WORKDIR /celery_app

CMD ["celery", "-A", "app.tasks", "flower"]
