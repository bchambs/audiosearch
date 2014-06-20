import json
import requests
import urllib
import requests
from requests import ConnectionError
from requests import HTTPError
from requests import TooManyRedirects
from time import sleep
from util import debug, debug_l

__all__ = ['ENCall']

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

        if method is 'profile' and call_type is 'artist':
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
                        debug_l(jobj['response']['status']['message'].lower())
                        raise ExceededCallLimit

                    return jobj['response'][self.type_key]

                # CATCH not json object
                except ValueError as e:
                    # repr(e)
                    debug_l('result not JSON...')
                    sleep(snooze)

            # CATCH requests error
            except ConnectionError as e:
                # repr(e)
                debug_l('connection error (?)')
                pass #handle this

            # CATCH http error
            except (HTTPError, TooManyRedirects) as e:
                # repr(e)
                debug_l('http problems...')
                sleep(snooze)

            # CATCH echo nest error
            except ExceededCallLimit as e:
                # repr(e)
                debug_l('malformed call')
                sleep(snooze)
                

            threshold += 2
            debug('threshold: %s' % threshold)
            if threshold is 4:
                raise CallTimedOut
                break
        

    class ExceededCallLimit(Exception):
        debug_l('ExceededCallLimit thrown.')
        pass

    class CallTimedOut(Exception):
        debug_l('CallTimedOut thrown.')
        pass

class AudiosearchConstants:
    ARTIST_PROFILE_B = [
        'biographies',
        'hotttnesss',
        'images',
        'terms',
    ]