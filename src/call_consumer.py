import json
import urllib
from time import sleep

import requests


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
        result : (string, dict) tuple
            if string is 'ready', dict contains completed ENCall
            otherwise dict is None
        """
        attempt = 0

        while True:
            try:
                resource = requests.get(package.url, params=package.payload)

                try:
                    resource_json = resource.json()

                    # branch by echo nest result code
                    code = resource_json['response']['status']['code']

                    # success
                    if code == ENConsumer.SUCCESS:
                        resource_dict = resource_json['response'][package.KEY_]
                        result = ("ready", resource_dict)

                        return result

                    # limit exceeded, snooze then retry
                    elif code == ENConsumer.LIMIT_EXCEEDED:
                        raise LimitError

                    # bad parameter
                    elif code == ENConsumer.MISSING_PARAM or code == ENConsumer.INVALID_PARAM:
                        result = ("Invalid request.", None)
                        return result

                    # unrecoverable error (bad key, unknown)
                    else:
                        result = ("Unrecoverable error.", None)
                        return result

                # CATCH result not json or corrupt
                except (ValueError, KeyError):
                    # TODO: log failure
                    result = ("Received an invalid response from the Echo Nest.", None)
                    return result

            # CATCH requests errors
            except requests.exceptions.RequestException:
                # TODO: log failure
                result = ("Unable to connect to the Echo Nest.", None)
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
                # TODO: log failure and handle this more appropriately
                result = ("Audiosearch is receiving too many requests!  Try again soon!", None)
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

