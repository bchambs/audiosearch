from __future__ import absolute_import

import json
import urllib
from time import sleep

import requests

from audiosearch.constants import CALL_LIMIT, SERVICE_TIMOUT_MSG
import src.services as services


class ENConsumer(object):

    # EchoNest response codes.
    SUCCESS = 0
    LIMIT_EXCEEDED = 3
    MISSING_PARAM = 4
    INVALID_PARAM = 5


    @staticmethod
    def consume(package):
        attempt = 0

        while attempt < CALL_LIMIT:
            try:
                response = requests.get(package.url, params=package.payload)
                json_response = response.json()

                # TODO: move key path to two static variables. 
                code = json_response['response']['status']['code']
                status_msg = json_response['response']['status']['message']

                # Received a valid response.  Raise exception if data is empty.
                if code == ENConsumer.SUCCESS:
                    data = json_response['response'][package.ECHO_NEST_KEY]

                    if len(data):
                        return data
                    else:
                        raise services.EmptyResponseError()

                # Exceeded API access limit.  Snooze then retry.
                elif code == ENConsumer.LIMIT_EXCEEDED:
                    attempt += 1
                    sleep(CALL_SNOOZE)

                # TODO: make this less fragile.  Check echo nest docs.
                elif "does not exist" in status_msg:
                    raise services.EmptyResponseError()

                # Received error code in response.
                else:
                    raise services.ServiceError(status_msg)

            # Invalid request or unable to parse json response.
            except (requests.RequestException, ValueError, KeyError) as e:
                raise services.ServiceError(e)

        # Service timed out.
        # TODO: move str to constants.py.
        raise services.ServiceError(SERVICE_TIMOUT_MSG)
        
