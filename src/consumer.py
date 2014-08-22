from __future__ import absolute_import

import json
import urllib
from time import sleep

import requests

from audiosearch import config as cfg
import src.services as services


class ENConsumer(object):

    # EchoNest result codes
    SUCCESS = 0
    LIMIT_EXCEEDED = 3
    MISSING_PARAM = 4
    INVALID_PARAM = 5


    @staticmethod
    def consume(package):
        attempt = 0

        while attempt < cfg.CALL_LIMIT:
            try:
                response = requests.get(package.url, params=package.payload)
                json_response = response.json()

                code = json_response['response']['status']['code']
                status_msg = json_response['response']['status']['message']

                # success, return echo nest resource
                if code == ENConsumer.SUCCESS:
                    data = json_response['response'][package.ECHO_NEST_KEY]

                    if len(data) < 1:
                        raise services.EmptyServiceResponse()

                    return data

                # exceeded api_key limit, snooze until timeout
                elif code == ENConsumer.LIMIT_EXCEEDED:
                    attempt += 1
                    sleep(CALL_SNOOZE)

                elif "does not exist" in status_msg:
                    raise services.EmptyServiceResponse()

                # call rejected by echo nest
                else:
                    raise services.EchoNestServiceFailure(json_response['response']['status']['message'])

            # invalid request or unable to parse json
            except (requests.RequestException, ValueError, KeyError) as e:
                raise EchoNestServiceFailure(e)

        # timeout
        raise services.EchoNestServiceFailure("Audiosearch is receiving too many requests.  Try again soon!")
        
