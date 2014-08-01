import json
import urllib
from time import sleep

import requests

import audiosearch.config as cfg
import utils
import services
# from services import EchoNestServiceFailure


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

                code = json_response['response']['status']['code']

                # success, return echo nest resource
                if code == ENConsumer.SUCCESS:
                    return json_response['response'][package.ECHO_NEST_KEY]

                # exceeded api_key limit, snooze until timeout
                elif code == ENConsumer.LIMIT_EXCEEDED:
                    attempt += 1
                    sleep(CALL_SNOOZE)

                # call rejected by echo nest
                else:
                    print "call rejected by echo nest"
                    raise services.EchoNestServiceFailure(json_response['response']['status']['message'])

            # invalid request or unable to parse json
            # except (requests.RequestException, ValueError, KeyError) as e:
            #     print "=====================invalid request or unable to parse json"
            #     raise EchoNestServiceFailure(e)
            except requests.RequestException as e:
                print "1::%s" % str(package)
                raise services.EchoNestServiceFailure(e)
            except ValueError as e:
                print "2::%s" % str(package)
                raise services.EchoNestServiceFailure(e)
            except KeyError as e:
                print "3::%s" % str(package)
                raise services.EchoNestServiceFailure(e)

        # timeout
        print "====================timeout"
        raise services.EchoNestServiceFailure("Audiosearch is receiving too many requests.  Try again soon!")
        
