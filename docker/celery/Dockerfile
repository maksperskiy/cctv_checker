FROM python:3.12 AS base

ENV TZ="Europe/Minsk"

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

FROM base

COPY docker/celery/requirements.txt /opt/app/

RUN apt -y update\
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && pip3 install --default-timeout=1200 torch --index-url https://download.pytorch.org/whl/cpu \
    && pip3 install albumentations
    

COPY src/ /opt/app
# RUN python manage.py collectstatic --noinput

# ENTRYPOINT [ "python", "manage.py", "runserver" ]
