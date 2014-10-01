from __future__ import absolute_import
import codecs
import cPickle as pickle
import json
import os

import redis

from audiosearch.utils.paginate import paginate


FAILED_KEYS = 'failed:keys'


class RedisCache(object):
    """Redis-py wrapper with cPickle serialization.  Echo requests which fail
    to return data (because of error or no results) are stored in a set keyed
    by ``FAILED_KEYS.``

    name: instance name
    params: RESOURCE_CACHE dict from audiosearch.conf.settings
    """

    def __init__(self, name, params):
        self.client_params = {
            'db': params.get('database', 0),
            'host': params.get('host'),
            'port': params.get('port'),
        }
        self.name = name

        try:
            self._pid = os.getpid()
        except os.OSError:
            self._pid = '????'

    def __contains__(self, key):
        # return False
        return self._cache.exists(key)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = redis.StrictRedis(**self.client_params)
        return self._client

    # General
    def delete(self, key):
        return self._cache.delete(key)

    def fetch(self, key, page):
        vtype = self._cache.type(key)

        if vtype == 'list':
            length = self.getlist_len(key)
            start, end = paginate(page, length)
            data = self.getlist(key, start, end)
        elif vtype == 'hash':
            data = self.gethash(key)
            length = 0
        else:
            raise ValueError()

        return (data, length)


    # Status checking
    def has_failed(self, key):
        return self._cache.sismember(FAILED_KEYS, key)

    def set_failed(self, key):
        return self._cache.sadd(FAILED_KEYS, key)


    # List
    def getlist(self, key, start, end):
        raw = self._cache.lrange(key, start, end)
        return [json.loads(element) for element in raw]

    def getlist_len(self, key):
        return self._cache.llen(key)

    def setlist(self, key, values):
        json_values = [json.dumps(element) for element in values]
        self._cache.rpush(key, *json_values)


    # Hash
    def gethash(self, key):
        return self._cache.hgetall(key)

    def sethash(self, key, value_map):
        self._cache.hmset(key, value_map)

    

    

    
