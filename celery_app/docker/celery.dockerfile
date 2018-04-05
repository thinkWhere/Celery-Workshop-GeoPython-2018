FROM python:3.6.4-alpine3.7

COPY . /celery_app

RUN pip install --upgrade pip

RUN apk update && \
 apk add python3 postgresql-libs && \
 apk add --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r /celery_app/requirements/celery_app.txt --no-cache-dir && \
 apk --purge del .build-deps

WORKDIR /celery_app

CMD ["celery", "-A", "app.tasks", "worker", "--loglevel=info"]
