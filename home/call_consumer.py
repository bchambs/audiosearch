import json
import urllib
from time import sleep

import requests

from home.util import debug

class ENConsumer(object):
    """
    Takes ENCall as input, consumes REST call, returns result or throws on fail.

    Error handling:
        Return a dict containing a status key detailing why the call failed.
        it is the client's responsibility to react to the status message.
    """

    # EchoNest result codes
    SUCCESS = 0
    LIMIT_EXCEEDED = 3
    MISSING_PARAM = 4
    INVALID_PARAM = 5


    @staticmethod
    def consume(package, snooze, limit):
        """
        Parameters
        ----------
        package : ENCall
           URL and query params used to consume Echo Nest REST service.
        snooze : int
            Time to sleep between failed consumptions.
        limit : int
            The number of attempts before a TimeOutError exception is thrown.

        Return value
        ------------
        result : dictionary
            Contains one or two keys:
                'status' = status of echo nest call
                package.METHOD = echo nest resource for package's method (profile, search, etc)
        """
        attempt = 0
        result = {'status': "failed"}

        while True:
            try:
                resource = requests.get(package.url, params=package.payload)

                try:
                    resource_json = resource.json()

                    # branch by echo nest result code
                    code = resource_json['response']['status']['code']

                    # success
                    if code == ENConsumer.SUCCESS:
                        if package.REDIS_ID:
                            result[package.REDIS_ID] = resource_json['response'][package.KEY_]
                        else:
                            result = resource_json['response'][package.KEY_]

                        result['status'] = "ready"
                        return result

                    # limit exceeded, snooze then retry
                    elif code == ENConsumer.LIMIT_EXCEEDED:
                        raise LimitError

                    # bad parameter
                    elif code == ENConsumer.MISSING_PARAM or code == ENConsumer.INVALID_PARAM:
                        result['message'] = "Invalid request."
                        return result

                    # unrecoverable error (bad key, unknown)
                    else:
                        result['message'] = "Unrecoverable error."
                        return result

                # CATCH result not json or corrupt
                except (ValueError, KeyError):
                    # TODO: log failure
                    result['message'] = "Received an invalid response from the Echo Nest."
                    return result

            # CATCH requests errors
            except requests.exceptions.RequestException:
                # TODO: log failure
                result['message'] = "Unable to connect to the Echo Nest."
                return result

            # CATCH echo nest limit exceeded
            except LimitError:
                attempt += 1

                if attempt == limit:
                    raise TimeOutErrorself

                else:
                    sleep(snooze)

            # CATCH exceeded attempt limit
            except TimeOutError:
                # TODO: log failure
                result['message'] = "Audiosearch is receiving too many requests!  Try again soon!"
                return result
        

class LimitError(Exception):
    pass
    # def __init__(self, value):
    #     self.value = value

    # def __str__(self):
    #     return repr(self.value)

class TimeOutError(Exception):
    pass
    # def __init__(self, value):
    #     self.value = value

    # def __str__(self):
    #     return repr(self.value)

