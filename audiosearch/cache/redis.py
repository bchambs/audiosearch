from __future__ import absolute_import
import ast
import os

import redis

from audiosearch.cache import base
from audiosearch.conf import messages


# TODO: make this a borg and remove singleton comments from base.py
class RedisCache(base.BaseCache):
    """Cache interface for views.py.  Exposes two public methods for getting
    and setting resource data.
    """

    def __init__(self, params):
        super(RedisCache, self).__init__(params)
        db = params.get('DATABASE', 0)
        timeout = params.get('CONNECTION_TIMEOUT')

        self._client_params = {
            'host': self._host,
            'port': self._port,
            'db': db,
            'socket_connect_timeout': timeout,
        }

        # TODO: remove (for debugging)
        try:
            self._pid = os.getpid()
        except os.OSError:
            self._pid = 'Unknown'


    def __repr__(self):
        indent = ' ' * 4
        title = "%s _ redis connection _ PID = %d:" % (self.name, self._pid)
        spec = ([("%s%s: %s") % (indent, k.upper(), v) for (k, v) in 
            self._client_params.items()])

        return '\n'.join([title] + spec)


    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = redis.StrictRedis(**self._client_params)
        return self._client


    @property
    def info(self):
        return self._client_params


    @property
    def name(self):
        return self._name


    def get(self, key, storage_type, start=None, end=None):
        try:
            if storage_type is list:
                value = self._get_list(key, start, end)
                size = self._get_list_size(key)
            elif storage_type is dict:
                pass
            else:   # Unexpected type
                raise base.UnexpectedTypeError
        except (redis.ResponseError, base.UnexpectedTypeError):
            # TODO: log this
            raise base.FailedResourceError(messages.STORAGE_FAILURE)
        else:
            return value, size


    def store(self, key, value):
        if type(value) is list:
            self._cache.rpush(key, *value)
        elif type(value) is dict:
            self._cachce.hmset(key, value)
        else:   # Unexpected type
            # log key, type
            pass    

        self._cache.expire(key, self.default_ttl)


    def _get_list(self, key, start=None, end=None):
        value = self._cache.lrange(key, start, end)
        if not value:
            raise base.MissingResourceError()
        return value


    def _get_list_size(self, key):
        return self._cache.llen(key)


    def delete(self, key):
        self._cache.delete(key)
