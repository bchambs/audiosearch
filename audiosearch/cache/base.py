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
    """API."""

    @property
    def info(): pass

    def delete(key): pass
    
    def gethash(key): pass
    
    def getlist(key, start=0, end=-1): pass

    def getlist_len(key): pass

    def has_failed(key): pass
    
    def set_failed(key): pass
    
    def store(key, value): pass
