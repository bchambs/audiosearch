from __future__ import absolute_import
from time import sleep

import requests

from audiosearch.constants import MSG_SERVICE_TIMOUT
from src import services

_ATTEMPT_LIMIT = 15
_CALL_SNOOZE = 2


# TODO: this doesnt need to be a class.
class ENConsumer(object):
    # EchoNest response codes.
    _SUCCESS = 0
    _LIMIT_EXCEEDED = 3
    _MISSING_PARAM = 4
    _INVALID_PARAM = 5


    @staticmethod
    def consume(package):
        attempt = 0

        while attempt < _ATTEMPT_LIMIT:
            try:
                print package.url
                response = requests.get(package.url, params=package.payload)
                json_response = response.json()

                # put this in the echo nest base service
                status_code = json_response['response']['status']['code']
                status_message = json_response['response']['status']['message']

                # Received a valid response.  Raise exception if data is empty.
                if status_code == ENConsumer._SUCCESS:
                    data = json_response['response'][package.ECHO_NEST_KEY]

                    if len(data):
                        return data
                    else:
                        raise services.EmptyResponseError()

                # Exceeded API access limit.  Snooze then retry.
                elif status_code == ENConsumer._LIMIT_EXCEEDED:
                    attempt += 1
                    sleep(_CALL_SNOOZE)

                # TODO: make this less fragile.  Check echo nest docs.
                elif "does not exist" in status_message:
                    raise services.EmptyResponseError()

                # Received error code in response.
                else:
                    raise services.ServiceError(status_message)

            # Invalid request or unable to parse json response.
            except (requests.RequestException, ValueError, KeyError) as e:
                raise services.ServiceError(e)

        # Service timed out.
        raise services.ServiceError(MSG_SERVICE_TIMOUT)
        