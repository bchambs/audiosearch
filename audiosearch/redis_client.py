'''
add fetch_all to pipeline the resource request list using 1 pipeline
    wrap fetch() with a pipeline param

create scheduled task to iterate over failed resources, try them again, and tally
    their total failed attempts
'''
from __future__ import absolute_import
import logging

import redis

from audiosearch.constants import (AVAIL, FAIL, PEND, NEW, MSG_NO_DATA, 
    MSG_UNEXPECTED_STORAGE_TYPE)


logger = logging.getLogger("general_logger")


# Redis client.
_HOST = 'localhost'
_PORT = 6379
_DATABASE = 0
_cache = redis.StrictRedis(host=_HOST, port=_PORT, db=_DATABASE)
_cache.client_setname("django_redis_client")

# Set of pending resource keys.
_PENDING_RESOURCES = '::PENDING_RESOURCES'
# Hash of 'resource key': 'error message' elements.
_FAILED_RESOURCES = '::FAILED_RESOURCES'


class UnexpectedTypeError(Exception):
    pass


class RedisDataType(object):
    """Redis data storage type enums."""
    # string_ = 'string'
    # list_ = 'list'
    # set_ = 'set'
    # zset_ = 'zset'
    # hash_ = 'hash'
    string_ = 0
    list_ = 1
    set_ = 2
    zset_ = 3
    hash_ = 4
_RDT = RedisDataType()


def fetch(key, ttl):
    """
    Refresh the time to live of key.
    Return a tuple of (status, value).  
    """

    global _cache
    count = 0

    with _cache.pipeline() as pipe:
        # Refresh ttl before assessing status.
        if ttl:
            pipe.expire(key, ttl).execute() 

        # Obtain value from cache at key.  If the Pending set or Failed hash
        # are modified in the body of the loop, the loop will restart to ensure
        # the block is atomic.  
        while True:
            count += 1
            try:
                pipe.watch(_PENDING_RESOURCES, _FAILED_RESOURCES)

                pipe.multi()
                pipe.sismember(_PENDING_RESOURCES, key)
                pipe.hexists(_FAILED_RESOURCES, key)
                pipe.exists(key)

                is_pending, has_failed, is_available = pipe.execute()

                if is_pending:
                    status = PEND
                    break

                elif has_failed:
                    status = FAIL
                    value = pipe.hget(_FAILED_RESOURCES, key)
                    break

                # Resource data is ready to be served.*  
                elif is_available:
                    value_type = pipe.type(key).execute().pop()

                    if value_type is _RDT.list_:
                        status = AVAIL
                        value = _cache.lrange(key, 0,-1)
                        break

                    elif value_type is _RDT.hash_:
                        status = AVAIL
                        value = _cache.hgetall(key)
                        break

                    # *Unexpected type.  This should only be raised if the Echo
                    # Nest API is updated.
                    else:
                        status = FAIL
                        value = MSG_NO_DATA
                        raise UnexpectedTypeError()

                # Resource is not in cache.
                else:
                    status = NEW
                    break

            # Pending set or Failed hash were modified during fetch.  Restart.
            # TODO: see if I can except on the key value which was modified.
            # If true, for Failed modifications break from the loop and return
            # the stored message as an error_message.  For Pending modications
            # return (PEND, None).
            except redis.WatchError:
                continue

            # TODO: see if storing a key in this scope raises watcherror.
            # If it does we need to use a lambda in an else statement.
            except UnexpectedTypeError:
                logger.error("Unexpected value type::%s, %s" %(key, value_type))
                break

    try:
        data = value
    except NameError:
        data = None

    print "loop count: %s" %count

    return status, data







def store(key, value, ttl):
    global _cache

    with _cache.pipeline() as pipe:
        while True:
            try:
                pipe.watch(_PENDING_RESOURCES, _FAILED_RESOURCES)

                pipe.multi()
                pipe.sismember(_PENDING_RESOURCES, key)
                pipe.hexists(_FAILED_RESOURCES, key)
                pipe.exists(key)

                is_pending, has_failed, is_available = pipe.execute()

                # key:value has been stored by another worker.
                if is_pending or has_failed or is_available:
                    break

                # Store key:value according to data type.
                elif type(value) is list:
                    _cache.rpush(key, *value)
                    break

                elif type(value) is dict:
                    _cache.hmset(key, value)
                    break

                # *Unexpected type.  This should only be raised if the Echo Nest
                # API is updated.
                else:
                    raise UnexpectedTypeError()

            # Pending set or Failed hash were modified during fetch.  Restart.
            except redis.WatchError:
                continue

            except UnexpectedTypeError:
                logger.error("Unexpected value type::%s, %s" %(key, value_type))
                break

    if ttl:
        _cache.expire(key, ttl)





