from __future__ import absolute_import
import threading


class Error():
    pass


class InvalidBackendError():
    pass


# TODO: django creates two threads which instantiate two cache connections.
# See if this occurs out of Test.  If so, enforce process-level singleton.
# class Singleton(object):
#     __singleton_lock = threading.Lock()
#     __singleton_instance = None
 
#     @classmethod
#     def instance(cls, params):
#         if not cls.__singleton_instance:
#             with cls.__singleton_lock:
#                 if not cls.__singleton_instance:
#                     cls.__singleton_instance = cls(params)

#         return cls.__singleton_instance

# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]


# class BaseCache(Singleton):
class BaseCache(object):
    """
    params: RESOURCE_CACHE dict from audiosearch.conf.settings.
    """

    # __metaclass__ = Singleton


    def __init__(self, params):
        try:
            self._name = params.pop('NAME')
            self._host = params.pop('HOST')
            self._port = params.pop('PORT')
        except KeyError:
            raise InvalidBackendError()
        else:
            self.default_ttl = params.get('DEFAULT_TTL', 300)
            self.persist_set = params.get('PERSIST_SET')


    def __contains__(self, key):
        return self._cache.exists(key)
