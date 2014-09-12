from __future__ import absolute_import
import ast
import os

import redis

from audiosearch.cache import base


class Error(Exception):
    pass


class UnexpectedTypeError(Exception):
    pass


class RedisCache(base.BaseCache):
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


    def get_list(self, key, start=0, end=-1):
        raw = self._cache.lrange(key, start, end)
        return [ast.literal_eval(i) for i in raw]


    def get_hash(self, key):
        raw = self._cache.hgetall(key)
        return ast.literal_eval(raw)


    def get(self, key, start, end):
        value_type = self._cache.type(key)

        if value_type == 'list':
            value = self.get_list(key, start, end)
        elif value_type == 'hash':
            value = self.get_hash(key)
        else:
            pass    # log key, type

        return value


    def store(self, key, value):
        if type(value) is list:
            self._cache.rpush(key, *value)
        elif type(value) is dict:
            self._cachce.hmset(key, value)
        else:   # Unexpected type
            pass    # log key, type

        self._cache.expire(key, self.default_ttl)






    # def get_list_many(self, keys, start=0, end=-1):
    #     hit = {}
    #     miss = set()

    #     for k in keys:
    #         value = self.get_list(k, start, end)

    #         if value:
    #             hit[k] = value
    #         else:
    #             miss.add(k)

    #     return hit, miss


    


    # def get(self, key):
    #     value = None

    #     if key in self._cache:
    #         type_ = self._cache.type(key)

    #         if type_ == 'list':
    #             value = self.get_list(key)
    #         elif type_ == 'hash':
    #             value = self.get_hash(key)
    #         else:
    #             raise UnexpectedTypeError(key)

    #     return value


    # def get_many(self, resources, start, end):
    #     hashes = []
    #     lists = []

    #     for res in resources:
    #         if res.type_ =


    #     ''''''''
    #     hit = {}
    #     miss = set()
    #     keys = set([res.key for res in resources])
        
    #     for k in keys:
    #         value = self.get(k)

    #         if value:
    #             hit[k] = value
    #         else:
    #             miss.add(k)

    #     return hit, miss

































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






    





