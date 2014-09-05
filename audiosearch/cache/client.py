from __future__ import absolute_import
import logging

import redis

from audiosearch import messages


logger = logging.getLogger("general_logger")

_LOOP_THRESHOLD = 10

# Key status constants.
_AVAIL = 'available'
_FAIL = 'failed'
_NEW = 'new'
_PEND = 'pending'

# Redis data type constants.
_LIST = 'list'
_HASH = 'hash'
_STRING = 'string'

# Connection setup.
_HOST = 'localhost'
_PORT = 6379
_DATABASE = 0



class Error(Exception):
    pass


class CacheClient(object):


    def __init__(self, uuid):
        self._client = redis.StrictRedis(host=_HOST, port=_PORT, db=_DATABASE)
        self._client.client_setname(uuid)

    def __str__(self):
        return self._client.get_clientname()

    def fetch(self, resources):
        wrap = {
            _AVAIL: list(),
            _FAIL: list(),
            _PEND: list(),
        }

        for res in resources:
            # status, data = self._fetch(res.key, res.ttl, miss=handler(res))
            # bundle = (res, data) if data else res
            # wrap[status].append(bundle)
            pass

        return  wrap[_AVAIL], wrap[_FAIL], wrap[_PEND]


    def _fetch(self, key, ttl, hit=None, miss=None):
        loop = -1

        with self.pipeline() as pipe:
            if ttl: pipe.expire(key, ttl).execute() 

            while True:
                loop += 1

                try:
                    pipe.watch(key)

                    if loop > _LOOP_THRESHOLD: raise CycleError()

                    is_pending = pipe.sismember(self.pending_pool, key)
                    has_failed = pipe.hexists(self.failed_pool, key)
                    exists = pipe.exists(key)

                    if is_pending:
                        status = _PEND
                        value = None
                        break

                    elif has_failed:
                        status = _FAIL
                        value = self.hget(self.failed_pool, key)
                        break

                    # Handle cache hit.
                    elif exists:
                        value_type = pipe.type(key)

                        pipe.multi()

                        if value_type == LIST_:
                            value = self.lrange(key, 0,-1)
                        elif value_type == HASH_:
                            value = self.hgetall(key)

                        status = _AVAIL
                        pipe.execute()
                        break

                    # Handle cache miss.
                    else:
                        try:
                            miss()
                        except TypeError:
                            status = _FAIL
                            value = messages.CONTENT_CREATION_FAIL
                            logger.exception("No miss handler.")
                        else:
                            status = _PEND
                            value = None
                        finally:
                            break

                except (CycleError, UnexpectedTypeError):
                    logger.exception(key)
                    status = _FAIL
                    value = messages.CONTENT_CREATION_FAIL
                    break

                except redis.WatchError:
                    logger.exception("WatchError in _fetch.")
                    continue

        print key
        print status
        return status, value






    





