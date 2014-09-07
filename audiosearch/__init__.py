from __future__ import absolute_import

from audiosearch.conf.settings import CACHE_CONFIG
from audiosearch.cache import RedisCache

Cache = RedisCache(CACHE_CONFIG)
