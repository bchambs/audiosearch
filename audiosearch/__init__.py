from __future__ import absolute_import

import redis

from audiosearch.cache import client
from audiosearch.celery import app as celery_app

cache = None

# 'Global' redis connection to be used in views.py.  We need to check if client
# exists because Django may import this module more than once during startup.
if not cache:
    print 1
    try:
        print 2
        cache = client.CacheClient('audiosearch')
        print 3
    except redis.ConnectionError:
        print 'Failed to establish cache connection.' # TODO: handle this.
