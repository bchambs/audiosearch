from __future__ import absolute_import

from celery import shared_task

from audiosearch import Cache
from audiosearch.models.service import (consume, ServiceFailureError, 
    TimeoutError)


@shared_task
def call_api(key, service):
    if service.dependency:
        print '\tfound dependency'
        try:
            intermediate = consume(service.dependency)
        except ServiceFailureError:
            return
        except TimeoutError:
            return
        req_fields = service.dependency.build(intermediate)
        service.payload.update(req_fields)
        print '\texiting dependency handling'

    try:
        echo_response = consume(service)
    except ServiceFailureError:
        print '\tservice error'
        return
    except TimeoutError:
        print '\ttimeout error'
        return
    else:
        try:
            data = service.process(echo_response)
        except AttributeError:
            data = echo_response

        Cache.store(key, data)


