FROM python:3.9
MAINTAINER Jiahao Zhang<jiahao.zhang@anu.edu.au>

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE app.settings

RUN mkdir -p /csmetrics
WORKDIR /csmetrics
ADD requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install --no-cache-dir gunicorn

ADD . /csmetrics
RUN python manage.py collectstatic --noinput

ENV GUNICORN_CMD_ARGS="--workers 32 --timeout 90 --graceful-timeout 90 --bind 0.0.0.0:8000"
ENTRYPOINT gunicorn $GUNICORN_CMD_ARGS app.wsgi
