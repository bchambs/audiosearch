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


class Error(Exception):
    pass


class ServiceFailureError(Error):
    pass


class TimeoutError(Error):
    pass


def consume(package):
    attempt = 0
    print package.url

    while True:
        try:
            if attempt > _ATTEMPT_LIMIT: raise TimeoutError()

            response = get(package.url, params=package.payload)
            json_response = response.json()

            status_code = json_response['response']['status']['code']
            status_message = json_response['response']['status']['message']

            # Response is valid, branch on echo nest code.
            if status_code == _SUCCESS:
                data = json_response['response'][package.ECHO_NEST_KEY]
                break

            # Exceeded API access limit.  Snooze then retry.
            elif status_code == _LIMIT_EXCEEDED:
                attempt += 1
                sleep(_CALL_SNOOZE)

            # TODO: make this less fragile.  Check echo nest docs.
            elif "does not exist" in status_message:
                # raise EchoCodeError(status_message)
                pass

            # Received error code in response.
            else:
                # raise EchoCodeError(status_code)
                pass

        # Invalid request or unable to parse json response.
        except (KeyError, RequestException, ValueError) as e:
            # raise NoDataError()
            pass
            break

        except TimeoutError:
            # raise NoDataError()
            pass
            break

    return data

    
