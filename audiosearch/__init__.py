from __future__ import absolute_import
import os

from audiosearch.cache.redis import RedisCache
from audiosearch.conf import settings
from audiosearch.conf.celery import app as celery_app


os.environ['CELERY_CONFIG_MODULE'] = 'audiosearch.conf.celery'

Cache = RedisCache('django', settings.CACHE_CONFIG)
