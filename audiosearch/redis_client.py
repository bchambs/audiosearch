from __future__ import absolute_import

import redis

from audiosearch.constants import HASH_, LIST_, N_CONTENT_ROWS, STRING_

# Key separator.
K_SEPARATOR = "::"

# Key statusus.
FAILED = "FAILED"
PENDING = "PENDING"

# Redis client.
_HOST = 'localhost'
_PORT = 6379
_DATABASE = 0
_cache = redis.StrictRedis(host=_HOST, port=_PORT, db=_DATABASE)
_cache.client_setname("django_redis_client")


def query(resources, n_items=None):
    global _cache

    n_items = n_items or N_CONTENT_ROWS     # Size of resource list to return.

    # Dict containing all available resources (cache hit). 
    # Key = resource object.  Value = redis value at resource.key.
    available = {}

    # List of unavailable resources grouped by status.
    failed = []    
    new = []
    pending = []  

    # If resource.key is in cache, branch by value type, and determine status.
    for resource in resources:
        key = resource.key

        # Refresh ttl.
        if resource.ttl:
            pipe = _cache.pipeline()
            pipe.expire(key, resource.TTL)
            pipe.exists(key)
            expire, hit = pipe.execute()
        else:
            hit = _cache.exists(key)

        if hit:
            d_type = resource.d_type
            template_id = resource.template_id

            if d_type == LIST_:
                available[resource] = _cache.lrange(key, 0,-1)

            elif d_type == STRING_:
                value = _cache.get(key)

                if value == PENDING:
                    pending.append(resource)
                elif value == FAILED:
                    failed.append(resource)
                else:
                    available[resource] = value

            elif d_type == HASH_:
                available[resource] = _cache.hgetall(key)
        else:
            new.append(resource)    

    return available, failed, new, pending



def store(key, value, ttl):
    global _cache

    if type(value) is list:
        _cache.rpush(key, *value)
    elif type(value) is str:
        _cache.set(str)
    elif type(value) is dict:
        _cache.hmset(key, value)

    if ttl:
        _cache.expire(key, ttl)





