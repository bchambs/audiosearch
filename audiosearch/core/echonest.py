from __future__ import absolute_import

import json
import time

import requests
from celery import shared_task, Task

from audiosearch.conf.tasks import SharedConnectionMixin
from audiosearch.core.exceptions import (DataKeyError, FatalStatusError,
                                        RateLimitError, UnexpectedFormatError)
from audiosearch.models.service import ServiceFactory

# Keyed status of an Echo Nest API call
# Location in JSON format: response['status']['code']
ECHONEST_STATUS_CODES = {
    '-1': 'Unknown Error',
    '0': 'Success',
    '1': 'Missing/ Invalid API Key',
    '2': 'This API key is not allowed to call this method',
    '3': 'Rate Limit Exceeded',
    '4': 'Missing Parameter',
    '5': 'Invalid Parameter',
}

# Echo Nest status codes which indicate the consumed service will never succeed
FATAL_STATUS_CODES = set([
    '-1',
    '1',
    '2',
    '4',
    '5',
    ])

# Status aliases
RATE_EXCEEDED = 3
SUCCESS = 0


def get_resource(key, category, content_type, params):
    """Create the services required to fulfill a resource request then
    defer the work to a celery worker."""

    service = ServiceFactory(category, content_type, params)
    call_echonest.delay(key, service)


class EchoNestAPICall(Task, SharedConnectionMixin):
    """Task definition and handlers for calling the Echo Nest's API."""

    abstract = True
    default_retry_delay = 2 # In seconds
    max_retries = 15

    # Set of execptions raised during task execution which indicate the service
    # will not succeed if retried
    fatal_errors = set([
        DataKeyError,
        FatalStatusError,
        requests.ConnectionError,
        requests.HTTPError,
        requests.TooManyRedirects,
        requests.Timeout,
        requests.URLRequired,
        requests.RequestException,    # Base requests exception
        UnexpectedFormatError,
        ValueError, # For requests.response to json conversion
        ])


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Called when task execution encounters an unhandled exception."""

        print 'in on_failure'
        print 'in on_failure'
        print 'in on_failure'
        print args
        print exc
        print
        print
        print
        
        if exc not in EchoNestAPICall.fatal_errors:
            # Unexpected exception. log
            pass

        # TODO: add case logic by exception
        #   -store key in failed set for bad requests
        #   -do something if echo nest host is down
        #   -do something if audiosearch host is down


    # def on_retry(self, exc, task_id, args, kwargs, einfo):
    #     pass


@shared_task(base=EchoNestAPICall, bind=True)
def call_echonest(self, key, service):
    """Attempt to retrieve Echo Nest data defined by `service` and store
    at Cache[`key`].  

    Explicitly handled exceptions indicate that the error may be temporary
    and that the task should be retried.

    Fatal errors are silently handled by on_failure().
    """
    
    print 1
    response = requests.get(service.url, params=service.payload)
    print 2
    response_dict = response.json()

    try:
        echonest_data = parse(response_dict, service.response_data_key)
        print 3
    except RateLimitError as e:
        raise self.retry(exc=e)

    resource_data = service.process(echonest_data)
    print 4
    self.Cache.store(key, resource_data)    # Raises StorageTypeError
    print 5



def parse(echonest_response, data_key):
    """Parse Echo Nest json response dict."""

    try:
        echonest_dict = echonest_response['response']
        status_code = echonest_dict['status']['code']
    except KeyError:
        raise UnexpectedFormatError()

    if status_code is SUCCESS:
        print 'SSSS'
        echonest_data = echonest_dict[data_key]
    elif status_code is RATE_EXCEEDED:
        print 'RRRR'
        raise RateLimitError()
    elif status_code in FATAL_STATUS_CODES:
        print 'FFFF'
        raise FatalStatusError(status_code)

    return echonest_data
