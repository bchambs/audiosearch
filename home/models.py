import json
import urllib
from time import sleep

import requests


"""
---------------------
audiosearch constants
---------------------
"""

ARTIST_BUCKET = [
    'biographies',
    'hotttnesss',
    'images',
    'terms',
    'songs',
    'hotttnesss_rank',
]

SIMILAR_BUCKET = [
    'familiarity_rank',
    'hotttnesss',
]

"""
-------------------
audiosearch classes
-------------------
"""

# Echo Nest call
class ENCall(object):
    LEAD = "http://developer.echonest.com/api"
    VERSION = "v4"
    QUERY_CONSTANTS = {
        "api_key": "QZQG43T7640VIF4FN",
        "format": "json"
    }
    SNOOZE = 2
    ATTEMPT_LIMIT = 5


    # form url without query string
    def __init__(self, call_type, method):
        self.ctype = call_type
        self.method = method
        self.path = '/'.join([ENCall.LEAD, ENCall.VERSION, self.ctype, self.method])
        self.id = ''
        self.data = {}

        if call_type == 'artist' and method == 'profile':
            self.type_key = 'artist'
        else:
            self.type_key = call_type + 's'

    # TODO: add url value to obj ?
    def __str__(self):
        return repr(self.id)


    # set query params to prepare call for consumption
    def build(self, EN_id, params=None, bucket=None):
        self.id = EN_id
        self.data.update(ENCall.QUERY_CONSTANTS)
        self.data['bucket'] = bucket

        if params:
            self.data.update(params)

        if self.method is 'search':
            self.data['name'] = EN_id
        else:
            self.data['id'] = EN_id


    """
    handle handling:
        return a dict containing a status key detailing why the call failed.
        it is the client's responsibility to react to the status message.
    """
    # consume call and return JSON
    def consume(self):
        threshold = 0
        result = {'status': 'failed'}

        while True:
            # attempt to consume REST call
            try:
                call = requests.get(self.path, params=self.data)

                try:
                    call_json = call.json()

                    # branch by echo nest result code
                    code = call_json['response']['status']['code']

                    # success
                    if code == 0:
                        # TODO: subclass ENCall according to method type.  
                        #   refactor common code to methods, pass dicts as results, set resulting json based on method type key ?
                        if self.method == 'similar':
                            result['similar']  = call_json['response'][self.type_key]
                        else:
                            result = call_json['response'][self.type_key]
                        result['status'] = 'ready'

                        return result

                    # limit exceeded, snooze then retry
                    elif code == 3:
                        raise LimitError

                    # bad parameter (TODO: this should be checked at instance creation)
                    elif code == 4 or code == 5:
                        result['message'] = 'Invalid request.'
                        return result

                    # unrecoverable error (bad key, unknown)
                    else:
                        result['message'] = 'Unrecoverable error.'
                        return result

                # CATCH result not json or corrupt
                except (ValueError, KeyError):
                    # TODO: log failure
                    result['message'] = 'Received an invalid response from the Echo Nest.'
                    return result

            # CATCH requests errors
            except requests.exceptions.RequestException:
                # TODO: log failure
                result['message'] = 'Unable to connect to the Echo Nest.'
                return result

            # CATCH echo nest limit exceeded
            except LimitError:
                threshold += 1

                if threshold == ENCall.ATTEMPT_LIMIT:
                    raise TimeOutError

                else:
                    sleep(ENCall.SNOOZE)

            # CATCH exceeded attempt limit
            except TimeOutError:
                # TODO: log failure
                result['message'] = 'Audiosearch is receiving too many requests!  Try again soon!'
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

