from __future__ import absolute_import
# import codecs
# import cPickle as pickle
import json
import os

import redis

from audiosearch.utils.paginate import paginate


FAILED_KEYS = 'failed:keys'


class RedisCache(object):
    """Redis-py wrapper with JSON serialization.  Echo requests which fail
    to return data (because of error or no results) are stored in a set keyed
    by ``FAILED_KEYS.``

    name: instance name
    params: RESOURCE_CACHE dict from audiosearch.conf.settings
    """

    def __init__(self, name, params):
        # Constructor args for redis-py
        self.client_params = {
            'db': params.get('database', 0),
            'host': params.get('host', 'localhost'),
            'port': params.get('port', 6379),
        }
        self.name = name
        try:
            self._pid = os.getpid()
        except os.OSError:
            self._pid = '????'

    def __contains__(self, key):
        return self._cache.exists(key)

    def __repr__(self):
        return "Cache: {} @ {}".format(self.name, self._pid)

    @property
    def _cache(self):
        """Force one instance per process."""
        if getattr(self, '_client', None) is None:
            self._client = redis.StrictRedis(**self.client_params)
        return self._client
    
    #######
    # API #
    #######

    # General
    def delete(self, key):
        return self._cache.delete(key)

    def fetch(self, key, page):
        """Return (value, length_of_value) tuple at cache[key]."""
        vtype = self._cache.type(key)

        if vtype == 'list':
            length = self.get_list_len(key)
            start, end = paginate(page, length)
            data = self.get_list(key, start, end)
        elif vtype == 'hash':
            data = self.get_hash(key)
            length = 0
        else:
            raise ValueError('Expecting dict or list, found: {}'.format(vtype))

        return (data, length)


    # Status checking
    def has_failed(self, key):
        return self._cache.sismember(FAILED_KEYS, key)

    def set_failed(self, key):
        return self._cache.sadd(FAILED_KEYS, key)


    # List
    def get_list(self, key, start, end):
        raw = self._cache.lrange(key, start, end)
        return [json.loads(element) for element in raw]

    def get_list_len(self, key):
        return self._cache.llen(key)

    def set_list(self, key, values):
        json_values = [json.dumps(element) for element in values]
        self._cache.rpush(key, *json_values)


    # Hash
    def get_hash(self, key):
        return self._cache.hgetall(key)

    def set_hash(self, key, value_map):
        self._cache.hmset(key, value_map)

    

    

    
