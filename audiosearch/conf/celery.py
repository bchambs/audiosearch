from __future__ import absolute_import
import os

import celery

from audiosearch.cache.redis import RedisCache
from audiosearch.conf import settings
from audiosearch.core.echonest import EchoNestAPICall


# Setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiosearch.conf.settings')
# app = celery.Celery('audiosearch', task_cls=EchoNestAPICall)
app = celery.Celery('audiosearch')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Config
BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['pickle', 'application/json']
CELERY_DISABLE_RATE_LIMITS = True
CELERY_IGNORE_RESULT = True   # Using task handlers requires saving result ?
# CELERY_IMPORTS = ("audiosearch.tasks", )
CELERY_IMPORTS = ('audiosearch.core.echonest',)
CELERY_RESULT_SERIALIZER = 'pickle'
CELERY_TASK_SERIALIZER = 'pickle'
CELERY_TIMEZONE = 'EST'
