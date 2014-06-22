import json
import urllib
from time import sleep

import requests
from requests import ConnectionError
from requests import HTTPError
from requests import TooManyRedirects

from util import debug

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
]

"""
-------------------
audiosearch classes
-------------------
"""

# Echo Nest call
class ENCall:
    LEAD = "http://developer.echonest.com/api"
    VERSION = "v4"

    QUERY_CONSTANTS = {
        "api_key": "QZQG43T7640VIF4FN",
        "format": "json"
    }


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


    # set query params to prepare call for consumption
    def build(self, EN_id, params=None, bucket=None):
        self.id = EN_id
        self.data.update(ENCall.QUERY_CONSTANTS)
        self.data['bucket'] = bucket

        if params:
            self.data.update(params)

        # redo this asap
        if self.method is 'search':
            self.data['name'] = EN_id
        else:
            self.data['id'] = EN_id


    # consume call and return JSON
    def consume(self):
        snooze = 2
        threshold = 0

        while True:
            try:
                res = requests.get(self.path, params=self.data)

                try:
                    jobj = res.json()

                    if jobj['response']['status']['code'] is not 0:
                        debug(jobj['response']['status']['code'])
                        raise ExceededCallLimit

                    return jobj['response'][self.type_key]

                # CATCH not json object
                except ValueError as e:
                    # repr(e)
                    debug('result not JSON...')
                    sleep(snooze)

            # CATCH requests error
            except ConnectionError as e:
                # repr(e)
                debug('connection error (?)')
                pass #handle this

            # CATCH http error
            except (HTTPError, TooManyRedirects) as e:
                # repr(e)
                debug('http problems...')
                sleep(snooze)

            # CATCH echo nest error
            except ExceededCallLimit as e:
                # repr(e)
                debug('malformed call')
                sleep(snooze)
            except KeyError as e:
                debug(repr(e))

            threshold += 2
            debug('threshold: %s' % threshold)
            if threshold is 6:
                raise CallTimedOut
                break
        

class ExceededCallLimit(Exception):
    debug('ExceededCallLimit thrown.')
    pass

class CallTimedOut(Exception):
    debug('CallTimedOut thrown.')
    pass

'''
HANDLE INDIVIDUAL EN ERROR CODES
'''
