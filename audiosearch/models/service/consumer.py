from __future__ import absolute_import
from time import sleep

from requests import get, RequestException


_ATTEMPT_LIMIT = 15
_CALL_SNOOZE = 2    # In seconds.

# EchoNest response codes.
_SUCCESS = 0
_LIMIT_EXCEEDED = 3
_MISSING_PARAM = 4
_INVALID_PARAM = 5


class EchoServiceError(Exception):
    pass


class ServiceFailureError(EchoServiceError):
    pass


class TimeoutError(EchoServiceError):
    pass


def consume(package):
    attempt = 1

    while 1:
        try:
            if attempt > _ATTEMPT_LIMIT: 
                raise TimeoutError()

            response = get(package.url, params=package.payload)
            json_response = response.json()
            status_code = json_response['response']['status']['code']

            # Response is valid, branch on echo nest code.
            if status_code == _SUCCESS:
                data = json_response['response'][package.echo_key]
            elif status_code == _LIMIT_EXCEEDED:
                attempt += 1
                sleep(_CALL_SNOOZE)
            else:
                raise ServiceFailureError()
                
        # Invalid request or unable to parse json response.
        except (KeyError, RequestException, ValueError):
            raise ServiceFailureError()
        else:
            return data

    
