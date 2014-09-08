from __future__ import absolute_import

from audiosearch.conf.settings import CACHE_CONFIG
from audiosearch.cache import InvalidBackendError, RedisCache


Cache = RedisCache(CACHE_CONFIG)

# Resource objects assume DEFAULT_TTL is defined if this passes on site setup.
try:
    DEFAULT_TTL = CACHE_CONFIG.pop('DEFAULT_TTL')
except KeyError:
    raise InvalidBackendError('Missing default TTL for cache keys')
