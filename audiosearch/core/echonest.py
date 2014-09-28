from __future__ import absolute_import
from itertools import chain

import requests
from celery import shared_task

from audiosearch import Cache
from audiosearch.conf import tasks
from audiosearch.core.exceptions import (
    FatalStatusError, 
    RateLimitError,
    UnexpectedFormatError, 
    UnexpectedTypeError)
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


def get(resource):
    prepared_request = prepare(resource)
    get_and_store(key, prepared_request)

def prepare(resource):
    payload = build_payload(resource.content, resource.params)
    url = build_url(resource.group, resource.method)
    return dict(url=url, params=payload, resp_key=resource.response_key)

def build_payload(buckets, params):
    payload = {
        'api_key': api.KEY,
        'bucket': buckets,
        'format': api.FORMAT,
    }
    return dict(chain(payload.iteritems(), params.iteritems()))

def build_url(group, method):
    return '/'.join([BASE_URL, group, method])


# Async
def failed_call(self, exc, task_id, args, kwargs, einfo):
    print 'in failed'

def parse(echo_response, response_key):
    try:
        echo_dict = echo_response['response']
        status_code = echo_dict['status']['code']
    except KeyError:
        raise UnexpectedFormatError('filtering response')

    if status_code is SUCCESS:
        try:
            echo_data = echo_dict[response_key]
        except KeyError:
            raise UnexpectedFormatError('response key')
        else:
            return echo_data

    elif status_code is RATE_EXCEEDED:
        raise RateLimitError()
    elif status_code in FATAL_STATUS_CODES:
        raise FatalStatusError(status_code)


def call_api(key, url, payload, response_key):
    response = requests.get(url, params=payload)
    response_dict = response.json()

    try:
        echodata = parse(response_dict, response_key)
    except FatalStatusError:
        raise
    except RateLimitError as e:
        raise call_api.retry(exc=e)
    except UnexpectedFormatError:
        raise

    return echodata



@shared_task(
    base=tasks.SharedConnection,
    # bind=True,
    default_retry_delay=2,
    max_retries=5,
    on_failure=failed_call)
def get_and_store():
    
