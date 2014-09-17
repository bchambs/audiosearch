from __future__ import absolute_import

from audiosearch.conf.settings import CACHE_CONFIG
from audiosearch.cache import InvalidBackendError, RedisCache
from audiosearch.celery import app as celery_app


Cache = RedisCache('django', CACHE_CONFIG)
try:
    DEFAULT_TTL = CACHE_CONFIG.pop('DEFAULT_TTL')
except KeyError:
    raise InvalidBackendError('Missing default TTL for cache keys')
