"""
TODO: create scheduled task to track cache hit / miss stats.
TODO: first action is to store key in pending set.
"""
from __future__ import absolute_import
import logging

from celery import shared_task

from audiosearch.cache.client import client
from audiosearch.services.services import EmptyResponseError, ServiceError


logger = logging.getLogger("general_logger")


# service.dependencies is a list of ()

@shared_task
def call_echo_nest(key, ttl, service, dependencies):

    print "hello"
    # try:
    #     # build a list of required services placing all dependncies in order use a helper function.
    #     if service.dependency:
    #         intermediate = ENConsumer.consume(service.dependency)
    #         service.combine_dependency(intermediate)

    #     echo_nest_response = ENConsumer.consume(service)

    #     try:
    #         data = service.process(echo_nest_response)
    #     except AttributeError:
    #         data = echo_nest_response

    # # Received error message in EchoNest response.
    # except ServiceError as err_msg:
    #     logger.warning("Service Failure::%s, %s" %(key, service))
    #     logger.warning("Error   Message::%s" %(err_msg))

    #     error_message = err_msg

    # # Service did not return results.  
    # except EmptyResponseError:
    #     error_message = constants.MSG_NO_DATA

    # data = data or error_message

    # client.store(key, data, service.ttl)



