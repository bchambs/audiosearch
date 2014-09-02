"""
TODO: create scheduled task to track cache hit / miss stats.
TODO: first action is to store key in pending set.
"""
from __future__ import absolute_import
import logging

from celery import shared_task

from audiosearch import messages
from audiosearch.cache.client import client
from audiosearch.services.base import EmptyResponseError, ServiceError
from audiosearch.services.consumer import consume
from audiosearch.services.dependency import DependencyError


logger = logging.getLogger("general_logger")

#todo redo tries
@shared_task
def call_echo_nest(key, ttl, service, dependencies):
    """


    CONSUME CAN RETURN EMPTY DATA CATCH THIS

    """
    print 1
    continue_task = client.establish_pending(key)
    print 2

    if not continue_task: return
    print 3

    if dependencies:
        try:
            _fulfill_dependencies(service, dependencies)
        except EmptyResponseError:
            client.establish_failed(key, messages.NO_DATA)
            return False
        except DependencyError:
            client.establish_failed(key, messages.CONTENT_CREATION_FAIL)
            logger.exception(key)
            return False
        except ServiceError as e:
            client.establish_failed(key, repr(e))
            logger.exception("%s: %s" %(key, repr(e)))
            return False
    print 4

    try:
        echo_nest_response = consume(service)
    except EmptyResponseError:
        client.establish_failed(key, messages.NO_DATA)
    except ServiceError as e:
        logger.exception("%s: %s" %(key, repr(e)))
        client.establish_failed(key, str(e))
    else:
        print 5

        try:
            data = service.process(echo_nest_response)
        except AttributeError:
            data = echo_nest_response
        print 6
        
        client.store(key, data, ttl)
        print 7


def _fulfill_dependencies(service, dependencies):
    for prereq in dependencies:
        intermediate = consume(prereq)
        required_fields = prereq.build(intermediate)
        service.payload.update(required_fields)




from time import sleep
@shared_task
def do_nothing(x):
    sleep(x)
    print "awake"
