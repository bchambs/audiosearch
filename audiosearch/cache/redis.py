"""
TODO: store artist / song hashes with form
    artist_hash::a {'artist 1': ECHO_HASH,...},
    song_hash::a {'title by artist 1': ECHO_HASH,...},
"""
from __future__ import absolute_import
import codecs
import cPickle
import os

import redis

from audiosearch.cache.base import BaseCache
from audiosearch.core.exceptions import StorageTypeError


_failed_keys = 'Failed keys'


class RedisCache(BaseCache):
    """Redis-py wrapper with cPickle serialization.  Echo requests which fail
    to return data (because of error or no results) are stored in a set keyed
    by ``_failed_keys.``

    Pending request handling: 
        The get_echo_data handler will execute a cached LUA script to determine
        if the request is in the task queue.  Pending keys are stored in a set
        keyed by ``_pending_keys.``  Logic should be something like:

        LUA (py syntax)
            1. if not cache[key] and 
                not cache.ismember(failed_keys, key) and 
                not cache.ismember(pending_keys, key):
                    cache.sadd(pending_keys, key)

                    return True

        CALLER
            2. if response is True enqueue task, else do not enqueue

        Store script in audiosearch/scripts.  In audiosearch/__init__ open,
        load, then 'cache' it in during RedisCache.__init__.  Add the hash as a
        static attribute so workers have access.

    name: instance name
    params: RESOURCE_CACHE dict from audiosearch.conf.settings
    """

    def __init__(self, name, params):
        # Kwargs for StrictRedis init
        self._spec = {
            'db': params.get('database', 0),
            'host': params.get('host'),
            'port': params.get('port'),
            'socket_connect_timeout': params.get('connection_timeout'),
        }
        self._name = name
        self.default_ttl = params.get('default_ttl', 300)
        self.persist_set = params.get('persist_set',set())

        try:
            self._pid = os.getpid()
        except os.OSError:
            self._pid = '????'


    def __repr__(self):
        """
        `instance name` redis connection @ `pid`
            `OPT`: `value`
            ...
        """
        indent = ' ' * 4
        specs = "{}{}: {}"
        title = "{} redis connection @ {}".format(self._name, self._pid)
        settings = [specs.format(indent, opt.upper(), value) 
                    for (opt, value) 
                    in self._spec.items()]
        return '\n'.join([title] + settings)


    def __contains__(self, key):
        yo = self._cache.__contains__(key)
        print '???'
        print self._cache.exists(key)
        print yo
        print self._cache.dbsize()
        print self._cache.keys()
        return self._cache.exists(key)


    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = redis.StrictRedis(**self._spec)
        return self._client


    @property
    def info(self):
        """Return redis client specification."""
        return repr(self)
        print self._spec
        return self._spec


    def delete(self, key):
        return self._cache.delete(key)


    def gethash(self, key):
        return self._cache.hgetall(key)
    

    def getlist(self, key, start=0, end=-1):
        return self._cache.lrange(key, start, end)
        # list_ = self._cache.lrange(key, start, end)
        # unpickled = cPickle.dumps(list_)
        # return [element.decode("UTF-8") for element in unpickled]


    def getlist_len(self, key):
        return self._cache.llen(key)


    def has_failed(self, key):
        return self._cache.sismember(_failed_keys, key)
    
    
    def set_failed(self, key):
        return self._cache.sadd(_failed_keys, key)
    

    def store(self, key, value):
        vt = type(value)

        if vt is list:
            self._cache.rpush(key, *value)
        elif vt is dict:
            self._cache.hmset(key, value)
        else:
            print vt
            print vt
            print vt
            print vt
            raise StorageTypeError()   

        self._cache.expire(key, self.default_ttl)


    ###############################
    ###############################
    ###############################
    ###############################
    ###############################
    def get_status(self, key):
        if key in self._cache:
            status = 'available'
        elif self.has_failed(key):
            status = 'failed'
        else:
            status = 'pending'

        return status
