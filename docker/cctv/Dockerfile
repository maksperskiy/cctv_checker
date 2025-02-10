FROM python:3.12 AS base

ENV TZ="Europe/Minsk"

WORKDIR /opt/app

FROM base

COPY docker/cctv/requirements.txt /opt/app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt -y update \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt 

COPY src/ /opt/app
# RUN python manage.py collectstatic --noinput

# ENTRYPOINT [ "python", "manage.py", "runserver" ]
