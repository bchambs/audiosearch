'''
move all of this to a handler
have the decorated task handle dependency check, have consume calls handled in private function
use a callback for dependencies?
'''
from __future__ import absolute_import

import celery

from audiosearch.cache.redis import RedisCache
from audiosearch.conf import settings


_ATTEMPT_LIMIT = 15
_CALL_SNOOZE = 2    # In seconds.


class CachePool(celery.Task):
    abstract = True
    _cache = None


    @property
    def Cache(self):
        if self._cache is None:
            self._cache = RedisCache(settings.CACHE_CONFIG)
        return self._cache


# @shared_task(base=CachePool, name='call api')
# def call_api(key, service):
#     if service.dependency:
#         try:
#             intermediate = consume(service.dependency)
#         except (ServiceFailureError, TimeoutError):
#             Cache.set_failed(key)
#             return 
#         req_fields = service.dependency.build(intermediate)
#         service.payload.update(req_fields)

#     try:
#         echo_response = consume(service)
#     except ServiceFailureError:
#         Cache.set_failed(key)
#     except TimeoutError:
#         Cache.set_failed(key)
#     else:
#         try:
#             data = service.process(echo_response)
#         except AttributeError:
#             data = echo_response

#         Cache.store(key, data)


