from __future__ import absolute_import


class Error():
    pass


class InvalidBackendError():
    pass


class BaseCache(object):
    """
    params: RESOURCE_CACHE dict from audiosearch.conf.settings.
    """
    def __init__(self, params):
        try:
            self._connection_name = params.pop('NAME')
            self._host = params.pop('HOST')
            self._port = params.pop('PORT')
        except KeyError:
            raise InvalidBackendError()
        else:
            self.default_ttl = params.get('DEFAULT_TTL', 300)


    def __contains__(self, key):
        return self.has_key(key)


    def has_key(self, key):
        return self.get(key) is not None


    def get(self, key):
        pass


    def set(self, key, value):
        pass


    def get_many(self, keys):
        pass


    def set_many(self, data):
        pass

    
