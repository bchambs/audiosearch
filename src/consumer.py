import json
import logging
import urllib
from time import sleep

import requests

import audiosearch.config as cfg
import src.util as util
from src.services import ENCallFailure


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

                print response.url

                if package.debug:
                    util.inspect_response(response, package.__class__)

                code = json_response['response']['status']['code']

                # success, return echo nest resource
                if code == ENConsumer.SUCCESS:
                    return json_response['response'][package.CALL_KEY]

                # exceeded api_key limit, snooze until timeout
                elif code == ENConsumer.LIMIT_EXCEEDED:
                    attempt += 1
                    sleep(CALL_SNOOZE)

                # call rejected by echo nest
                else:
                    raise ENCallFailure(json_response['response']['status']['message'])

            # invalid request or unable to parse json
            except (requests.RequestException, ValueError, KeyError) as e:
                raise ENCallFailure(e)

        # timeout
        raise ENCallFailure("Audiosearch is receiving too many requests.  Try again soon!")
        
