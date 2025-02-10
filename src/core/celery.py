from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.signals import setup_logging

# Set the default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("cctv")

app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django app configs
app.config_from_object("django.conf:settings", namespace="CELERY")


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa

    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


app.autodiscover_tasks()
