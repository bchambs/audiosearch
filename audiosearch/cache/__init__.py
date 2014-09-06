from __future__ import absolute_import

from audiosearch.cache import redis as redis_
from audiosearch

cache = redis_.RedisCache()
