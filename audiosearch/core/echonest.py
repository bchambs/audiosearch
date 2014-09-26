from __future__ import absolute_import

import requests
from celery import shared_task

from audiosearch.conf import tasks
from audiosearch.core.exceptions import (
    FatalStatusError, 
    RateLimitError,
    UnexpectedFormatError, 
    UnexpectedTypeError,
    )
from audiosearch.models import services


# Response codes indicating the consumed service will never succeed
FATAL_STATUS_CODES = set(['-1', '1', '2', '4', '5'])

# Status aliases
RATE_EXCEEDED = 3
SUCCESS = 0


def get(resource):
    key = resource.key
    group = resource.group
    method = resource.method
    params = resource.spec
    service = services.factory(group, method, params)

    print 'calling api'
    call_api.delay(key, service)


def failed(self, exc, task_id, args, kwargs, einfo):
    print 'in failed'


def parse(echonest_response, data_key):
    print 'in parse'
    try:
        echonest_dict = echonest_response['response']
        status_code = echonest_dict['status']['code']
    except KeyError:
        raise UnexpectedFormatError()

    if status_code is SUCCESS:
        echonest_data = echonest_dict[data_key]
    elif status_code is RATE_EXCEEDED:
        raise RateLimitError()
    elif status_code in FATAL_STATUS_CODES:
        raise FatalStatusError(status_code)

    return echonest_data


@shared_task(
    base=tasks.SharedConnection,
    bind=True,
    default_retry_delay=2,
    max_retries=5,
    on_failure=failed)
def call_api(self, key, service):
    print 'in call'
    response = requests.get(service.url, params=service.payload)
    response_dict = response.json()

    try:
        echonest_data = parse(response_dict, service.response_key)
    except RateLimitError as e:
        raise self.retry(exc=e)

    resource_data = service.process(echonest_data)
    self.Cache.store(key, resource_data)
