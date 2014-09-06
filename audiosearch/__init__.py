from __future__ import absolute_import

import redis

from audiosearch.redis.cache import AudiosearchCache
from audiosearch.celery import app as celery_app

django_cache_conn = None

if not django_cache_conn:
    # print 1
    try:
        # print 2
        django_cache_conn = CacheConnection()
        # print 3
    except redis.ConnectionError:
        print 'Failed to establish cache connection.' # TODO: handle this.
