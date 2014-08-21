from __future__ import absolute_import
import os

from django.conf import settings
from celery import Celery


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'audiosearch.settings')
app = Celery('audiosearch')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Disable celery logging from vmihailenco's github.
CELERYD_HIJACK_ROOT_LOGGER = False
 
def setup_task_logger(logger=None, **kwargs):
    logger.propagate = 1
 
from celery import signals
signals.setup_logging.connect(lambda **kwargs: True)
signals.after_setup_task_logger.connect(setup_task_logger)




