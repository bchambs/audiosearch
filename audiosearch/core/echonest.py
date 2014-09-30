from __future__ import absolute_import

import requests

from audiosearch.core.exceptions import (
    APIConnectionError,
    APIResponseError,
    RateLimitError)
from audiosearch.conf import api


# API config
API = 'api'
VERSION = 'v4'
HOST = 'http://developer.echonest.com'
BASE_PATH = '/'.join([API, VERSION])
BASE_URL = '/'.join([HOST, BASE_PATH])

# Response codes indicating the consumed service will never succeed
FATAL_STATUS_CODES = set(['-1', '1', '2', '4', '5'])

# Status aliases
RATE_EXCEEDED = 3
SUCCESS = 0

# Largest possible length of response data list
MAX_RESULTS = 100   


def call(group, method, params):
    url = '/'.join([BASE_URL, group, method])
    payload = prepare(params)

    try:
        response = requests.get(url, params=payload)
        response_dict = response.json()
    except requests.RequestException:
        raise APIConnectionError('unable to contact echo nest')
    except ValueError:
        raise APIResponseError('response not json')

    return response_dict

def parse(raw_response, method_key):
    try:
        response = raw_response['response']
        status = response['status']
        status_code = status['code']
    except KeyError:
        raise APIResponseError('unexpected format')

    if status_code is SUCCESS:
        try:
            echodata = response[method_key]
        except KeyError:
            raise APIResponseError('invalid data key')
        return echodata

    elif status_code is RATE_EXCEEDED:
        raise RateLimitError()
    else:
        raise APIResponseError(status)

def init_prepare(key, format):
    def _prepare(params):
        return dict(params.iteritems(), api_key=key, format=format)
    return _prepare

prepare = init_prepare(api.KEY, api.FORMAT)
