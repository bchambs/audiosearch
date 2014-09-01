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
HASH_ = 'hash'
STRING_ = 'string'

_LOOP_THRESHOLD = 10


class Error(Exception):
    pass

class CycleError(Error):
    pass

class DuplciateStorageError(Error):
    pass

class UnexpectedTypeError(Error):
    pass


class AudiosearchCache(redis.StrictRedis):
    _HOST = 'localhost'
    _PORT = 6379
    _DATABASE = 0


    def __init__(self):
        super(AudiosearchCache, self).__init__(host=self._HOST, port=self._PORT, 
            db=self._DATABASE)

        # Set of pending resource keys.
        self._pending_pool_key = '::PENDING_KEYS::'

        # Hash of 'resource key': 'error message' elements.
        self._failed_pool_key = '::FAILED_KEYS::'

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
                status, data = self._fetch(item.key, item.ttl, 
                    miss=item.handle_miss)

            except CycleError:
                logger.exception(item.key)
                bundle = item.key, messages.CONTENT_CREATION_FAIL
                wrap[_FAIL].append(bundle)

            except UnexpectedTypeError:
                logger.exception(item.key)
                bundle = item.key, messages.CONTENT_CREATION_FAIL
                wrap[_FAIL].append(bundle)

            else:
                if status == _AVAIL:
                    wrap[_AVAIL].append((item, data))
                elif status == _FAIL:
                    wrap[_FAIL].append((item, data))
                else:
                    wrap[_PEND].append(item.key)

        return  wrap[_AVAIL], wrap[_FAIL], wrap[_PEND]


    def store(self, key, value, ttl):
        loop_counter = -1

        with self.pipeline() as pipe:
            while True:
                loop_counter += 1
                if loop_counter > _LOOP_THRESHOLD: raise CycleError()

                try:
                    pipe.watch(key)

                    has_failed = pipe.hexists(self.failed_pool, key)
                    exists = pipe.exists(key)

                    if has_failed: 
                        break

                    elif exists:
                        value_type = pipe.type(key)

                        if value_type != LIST_ or value_type != HASH_:
                            raise UnexpectedTypeError()
                    
                    pipe.multi()

                    if type(value) is list:
                        pipe.rpush(key, *value)
                    elif type(value) is dict:
                        pipe.hmset(key, value)
                    else:
                        raise UnexpectedTypeError()

                    if ttl: pipe.expire(key, ttl)
                    pipe.srem(self.pending_pool, key)
                    pipe.execute()
                    break

                # Pending set or Failed hash were modified during fetch.  Restart.
                except redis.WatchError:
                    logger.exception("WatchError in store.")
                    continue

                # This should only be raised if the Echo Nest API is updated.
                except UnexpectedTypeError:
                    logger.exception(key)
                    break


    def establish_pending(self, key):
        loop_counter = -1

        with self.pipeline() as pipe:
            while True:
                loop_counter += 1
                if loop_counter > _LOOP_THRESHOLD: raise CycleError()

                try:
                    pipe.watch(key)

                    is_pending = pipe.sismember(self.pending_pool, key)
                    has_failed = pipe.hexists(self.failed_pool, key)
                    exists = pipe.exists(key)

                    if is_pending or has_failed or exists: 
                        return False
                    else:
                        self.sadd(self.pending_pool, key)
                        return True
                    
                except CycleError:
                    logger.exception(key)
                    return False

                except DuplciateStorageError:
                    logger.exception(key)
                    return False

                # Pending set or Failed hash were modified during fetch.  Restart.
                except redis.WatchError:
                    logger.exception("WatchError in establish_pending.")
                    continue


    def establish_failed(self, key, error_message):
        pipe = self.pipeline()
        pipe.hset(self.failed_pool, key, error_message)
        pipe.srem(self.pending_pool, key)
        pipe.execute()


    def _fetch(self, key, ttl, hit=None, miss=None):
        loop_counter = -1

        with self.pipeline() as pipe:
            if ttl: pipe.expire(key, ttl).execute() 

            while True:
                loop_counter += 1
                if loop_counter > _LOOP_THRESHOLD: raise CycleError()

                try:
                    pipe.watch(key)

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

                except redis.WatchError:
                    logger.exception("WatchError in _fetch.")
                    continue

        return status, value


client = AudiosearchCache()





    





