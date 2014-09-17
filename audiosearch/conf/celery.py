from __future__ import absolute_import
import os
# from datetime import timedelta

from django.conf import settings
from celery import Celery

# Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiosearch.conf.settings')
app = Celery('audiosearch')

# app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Celery config
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True
# CELERY_IMPORTS = ("audiosearch.tasks", )
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'EST'


# Scheduled task config
# CELERYBEAT_SCHEDULE = {
#     'dbsize-tracker': {
#         'task': 'src.tasks.log_dbsize',
#         'schedule': timedelta(hours=1),
#     },
# }
