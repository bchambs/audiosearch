from __future__ import absolute_import
import codecs
import cPickle as pickle
import os

import redis

from audiosearch.core.exceptions import UnexpectedTypeError


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
        return self._cache.exists(key)

    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = redis.StrictRedis(**self.client_params)
        return self._client

    def delete(self, key):
        return self._cache.delete(key)

    def gethash(self, key):
        return self._cache.hgetall(key)

    def getlist(self, key, start=0, end=-1):
        raw = self._cache.lrange(key, start, end)
        deserialized = [pickle.loads(item) for item in raw]
        return [element.decode("UTF-8") for element in deserialized]

    def getlist_len(self, key):
        return self._cache.llen(key)

    def has_failed(self, key):
        return self._cache.sismember(FAILED_KEYS, key)
    
    def set_failed(self, key):
        return self._cache.sadd(FAILED_KEYS, key)

    def store(self, key, value):
        vtype = type(value)

        if vtype is list:
            encoded = [element.encode("UTF-8") for element in value]
            serialized = [pickle.dumps(item) for item in encoded]
            self._cache.rpush(key, *serialized)
        elif vtype is dict:
            self._cache.hmset(key, value)
        else:
            raise UnexpectedTypeError(key, vtype)   
