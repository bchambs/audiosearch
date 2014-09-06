from __future__ import absolute_import

import redis

from audiosearch.cache import base

class RedisCache(base.BaseCache):
    def __init__(self, params):
        super(RedisCache, self).__init__(params)
        db = params.get('DATABASE', 0)
        self._client_kwargs = dict(host=self._host, port=self._port, db=db)


    @property
    def _cache(self):
        if getattr(self, '_client', None) is None:
            self._client = redis.StrictRedis(self._client_kwargs)
        return self._client


    def get(self, key):
        pass

    def set(self, key, value):
        pass

    def get_many(self, keys):
        d = {}
        for k in keys:
            val = self.get(k)
            if val is not None:
                d[k] = val
        return d

    def set_many(self, data):
        for key, value in data.items():
            self.set(key, value)



































class CacheConnection(object):

    def __init__(self):
        self._client = redis.StrictRedis(host=_HOST, port=_PORT, db=_DATABASE)


    def fetch(self, key, ttl, miss=None):
        loop = -1
        
        with self._client.pipeline() as pipe:
            if ttl: pipe.expire(key, ttl).execute()

            while 1:
                loop += 1

                try:
                    if loop > _LOOP_THRESHOLD: raise CycleError()

                    pipe.watch(key)

                    hit = pipe.exists(key)
                    if hit:
                        value_type = pipe.type(key)

                        pipe.multi()

                        if value_type == 'list':
                            value = self.lrange(key, 0,-1)
                        elif value_type == 'hash':
                            value = self.hgetall(key)
                        else:
                            raise UnexpectedTypeError()
                    else:
                        pipe.reset()
                        raise KeyNotFoundError()
                        break

                except (CycleError, UnexpectedTypeError):
                    pipe.reset()
                    break
                except redis.WatchError:
                    continue

                else:
                    print 'in else'
                    return value
        print 'outside loop ??'



''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

    # if ttl: pipe.expire(key, ttl).execute()

    # while 1:
    #     loop += 1

    #     try:
    #         if loop > _LOOP_THRESHOLD: raise CycleError()

    #         pipe.watch(key)

    #         hit = pipe.exists(key)

    #         if hit:
    #             value_type = pipe.type(key)

    #             pipe.multi()

    #             if value_type == LIST_:
    #                 value = self.lrange(key, 0,-1)
    #             elif value_type == HASH_:
    #                 value = self.hgetall(key)
    #             else:
    #                 raise UnexpectedTypeError()

    #         else:
    #             pass

    #     except CycleError:
    #         pass
    #     except UnexpectedTypeError:
    #         pass
    #     except redis.WatchError:
    #         pass


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

                # Handle cache hit.
    #             elif exists:
    #                 value_type = pipe.type(key)

    #                 pipe.multi()

    #                 if value_type == LIST_:
    #                     value = self.lrange(key, 0,-1)
    #                 elif value_type == HASH_:
    #                     value = self.hgetall(key)

    #                 status = _AVAIL
    #                 pipe.execute()
    #                 break

    #             # Handle cache miss.
    #             else:
    #                 try:
    #                     miss()
    #                 except TypeError:
    #                     status = _FAIL
    #                     value = messages.CONTENT_CREATION_FAIL
    #                     logger.exception("No miss handler.")
    #                 else:
    #                     status = _PEND
    #                     value = None
    #                 finally:
    #                     break

    #         except (CycleError, UnexpectedTypeError):
    #             logger.exception(key)
    #             status = _FAIL
    #             value = messages.CONTENT_CREATION_FAIL
    #             break

    #         except redis.WatchError:
    #             logger.exception("WatchError in _fetch.")
    #             continue

    # print key
    # print status
    # return status, value






    





