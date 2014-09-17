from __future__ import absolute_import

import celery
import requests

from audiosearch.core import tasks
from audiosearch.models.service import ServiceFactory


# EchoNest response codes.
_SUCCESS = 0
_LIMIT_EXCEEDED = 3
_MISSING_PARAM = 4
_INVALID_PARAM = 5


class EchoResponseError(Exception):
    pass


class RateLimitError(EchoResponseError):
    pass


def get_data(key, category, content, params):
    service = ServiceFactory(category, content, params)
    tasks.call_echo_api.delay(key, service, service.dependencies)


# TODO: move key arg to a callback or use celery on_success / on_fail functions
@celery.shared_task(base=tasks.CachePool)
def call_api(key, service, dependencies=None):
    if dependencies:
        for service in dependencies:
            pass
    pass


def parse_response():
    """Parse echo nest REST api response and return the call's data element as
    a dict.
    """



# def consume(package):
#     attempt = 1

#     while 1:
#         try:
#             if attempt > _ATTEMPT_LIMIT: 
#                 raise TimeoutError()

#             response = get(package.url, params=package.payload)
#             json_response = response.json()
#             status_code = json_response['response']['status']['code']

#             # Response is valid, branch on echo nest code.
#             if status_code == _SUCCESS:
#                 data = json_response['response'][package.echo_key]
#             elif status_code == _LIMIT_EXCEEDED:
#                 attempt += 1
#                 sleep(_CALL_SNOOZE)
#             else:
#                 raise ServiceFailureError()
                
#         # Invalid request or unable to parse json response.
#         except (KeyError, RequestException, ValueError):
#             raise ServiceFailureError()
#         else:
#             return data
