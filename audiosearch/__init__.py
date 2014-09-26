from __future__ import absolute_import
import os

from audiosearch.conf import settings
from audiosearch.cache import InvalidBackendError, RedisCache
from audiosearch.conf.celery import app as celery_app


os.environ['CELERY_CONFIG_MODULE'] = 'audiosearch.conf.celery'

Cache = RedisCache('django', settings.CACHE_CONFIG)
try:
    DEFAULT_TTL = settings.CACHE_CONFIG.pop('default_ttl')
except KeyError:
    raise InvalidBackendError('Missing default time to live for cache keys')
