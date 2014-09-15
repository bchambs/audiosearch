from __future__ import absolute_import


class CacheError(Exception):
    pass


class FailedResourceError(CacheError):
    pass


class InvalidBackendError(CacheError):
    pass


class MissingResourceError(CacheError):
    pass


class UnexpectedTypeError(CacheError):
    pass


class BaseCache(object):
    """
    params: RESOURCE_CACHE dict from audiosearch.conf.settings.
    """

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
