FROM python:3.6.4-alpine3.7

ADD . /flower_app

RUN pip install -r /flower_app/requirements.txt

WORKDIR /flower_app

CMD ["flower", ""]
