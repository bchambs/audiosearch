from __future__ import absolute_import


# Echo Nest API calls
class EchoNestResponseError(Exception):
    pass

class RateLimitError(EchoNestResponseError):
    pass

class UnexpectedFormatError(EchoNestResponseError):
    pass


# Services for requesting Echo Nest data
class ServiceError(Exception):
    pass

class DependencyError(ServiceError):
    pass

class DataKeyError(ServiceError):
    # invalid data key used in successful echonest response dicts
    pass

class FatalStatusError(ServiceError):
    pass


# Cache
class CacheError(Exception):
    pass

class StorageTypeError(CacheError):
    pass
