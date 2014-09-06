from __future__ import absolute_import


class Error():
    pass


class InvalidBackendError():
    pass


# TODO: replace bodies with pass and implement in sub using pipes.
class BaseCache(object):
    """
    params: RESOURCE_CACHE dict from audiosearch.settings.
    """
    def __init__(self, params):
        try:
            self._host = params.pop('HOST')
            self._port = params.pop('PORT')
        except KeyError:
            raise InvalidBackendError()
        else:
            self.timeout = params.get('TIMEOUT', 0)    # Persist if no timeout.

    def __contains__(self, key):
        return self.get(key) is not None


    def get(self, key):
        pass

    def set(self, key, value):
        pass

    def get_many(self, keys):
        pass

    def set_many(self, data):
        pass

    
