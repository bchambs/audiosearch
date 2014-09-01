from __future__ import absolute_import
import logging

import redis

from audiosearch import messages


logger = logging.getLogger("general_logger")

# Key status constants.
_AVAIL = 'available'
_FAIL = 'failed'
_NEW = 'new'
_PEND = 'pending'

# Redis data type constants.
LIST_ = 'list'
HASH_ = 'dict'


class UnexpectedTypeError(Exception):
    pass

class AudiosearchCache(redis.StrictRedis):
    _HOST = 'localhost'
    _PORT = 6379
    _DATABASE = 0


    def __init__(self):
        super(AudiosearchCache, self).__init__(host=self._HOST, port=self._PORT, 
            db=self._DATABASE)

        # Set of pending resource keys.
        self._pending_pool_key = '::PENDING_KEYS'

        # Hash of 'resource key': 'error message' elements.
        self._failed_pool_key = '::FAILED_KEYS'

    def __str__(self):
        return self._client.get_clientname() or ''

    @property
    def pending_pool(self):
        return self._pending_pool_key

    @property
    def failed_pool(self):
        return self._failed_pool_key



    def fetch_all(self, content):
        wrap = {
            _AVAIL: list(),
            _FAIL: list(),
            _PEND: list(),
        }

        for item in content:
            try:
                status, data = self._fetch(item.key, item.ttl, miss=item.handle_miss)
            except UnexpectedTypeError:
                logger.error("Unexpected value type: %s" %(item.key))
                wrap[_FAIL].append(item.key, messages.CONTENT_CREATION_FAIL)
            else:
                if status == _AVAIL:
                    wrap[_AVAIL].append((item.key, data))
                elif status == _FAIL:
                    wrap[_FAIL].append((item.key, data))
                else:
                    wrap[_PEND].append(item.key)

        return  wrap[_AVAIL], wrap[_FAIL], wrap[_PEND]



    def _fetch(self, key, ttl, hit=None, miss=None):
        with self.pipeline() as pipe:
            if ttl:
                pipe.expire(key, ttl).execute() 

            while True:
                try:
                    pipe.watch(key)

                    pipe.multi()
                    pipe.sismember(self.pending_pool, key)
                    pipe.hexists(self.failed_pool, key)
                    pipe.exists(key)

                    is_pending, has_failed, is_available = pipe.execute()

                    if is_pending:
                        status = _PEND
                        value = None
                        break

                    elif has_failed:
                        status = _FAIL
                        value = self.hget(self.failed_pool, key)
                        break

                    # Resource data is ready to be served.*  
                    elif is_available:
                        value_type = pipe.type(key).execute().pop()

                        if value_type == LIST_:
                            status = _AVAIL
                            value = self.lrange(key, 0,-1)
                            break

                        elif value_type == HASH_:
                            status = _AVAIL
                            value = self.hgetall(key)
                            break

                        # *Unexpected type.  This should only be raised if the 
                        # Echo Nest API is updated.
                        else:
                            raise UnexpectedTypeError()

                    # Resource is not in cache.
                    else:
                        # miss()
                        status = _PEND
                        value = None
                        # try:
                        #     print "resource is not in cache."
                        #     miss()
                        #     status = _PEND
                        #     value = None
                        # except TypeError:
                        #     status = _FAIL
                        #     value = messages.CONTENT_CREATION_FAIL
                        # break

                # Pending set or Failed hash were modified during fetch.  Restart.
                # TODO: see if I can except on the key value which was modified.
                # If true, for Failed modifications break from the loop and return
                # the stored message as an error_message.  For Pending modications
                # return (PEND, None).
                except redis.WatchError:
                    continue

        return status, value

client = AudiosearchCache()





# def store(key, value, ttl):
#     global _cache

#     with _cache.pipeline() as pipe:
#         while True:
#             try:
#                 pipe.watch(_PENDING_RESOURCES, _FAILED_RESOURCES)

#                 pipe.multi()
#                 pipe.sismember(_PENDING_RESOURCES, key)
#                 pipe.hexists(_FAILED_RESOURCES, key)
#                 pipe.exists(key)

#                 is_pending, has_failed, is_available = pipe.execute()

#                 # key:value has been stored by another worker.
#                 if is_pending or has_failed or is_available:
#                     break

#                 # Store key:value according to data type.
#                 elif type(value) is list:
#                     _cache.rpush(key, *value)
#                     break

#                 elif type(value) is dict:
#                     _cache.hmset(key, value)
#                     break

#                 # *Unexpected type.  This should only be raised if the Echo Nest
#                 # API is updated.
#                 else:
#                     raise UnexpectedTypeError()

#             # Pending set or Failed hash were modified during fetch.  Restart.
#             except redis.WatchError:
#                 continue

#             except UnexpectedTypeError:
#                 logger.error("Unexpected value type::%s, %s" %(key, value_type))
#                 break

#     if ttl:
#         _cache.expire(key, ttl)





