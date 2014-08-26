from __future__ import absolute_import
import logging

from celery import shared_task
from redis import WatchError

from audiosearch.redis_client import store
from src.consumer import ENConsumer
from src.services import EmptyResponseError, ServiceError


logger = logging.getLogger("general_logger")


@shared_task
def call_echo_nest(key, service, ttl):
    try:
        if service.dependency:
            intermediate = ENConsumer.consume(service.dependency)
            service.combine_dependency(intermediate)

        echo_nest_response = ENConsumer.consume(service)

        try:
            data = service.process(echo_nest_response)
        except AttributeError:
            data = echo_nest_response

    # Received error message in EchoNest response.
    except ServiceError as err_msg:
        logger.warning("Service Failure::%s, %s" %(key, service))
        logger.warning("Error   Message::%s" %(err_msg))

        error_message = err_msg

    # Service did not return results.  
    except EmptyResponseError:
        error_message = MSG_NO_DATA

    data = data or error_message

    store(key, data, ttl)




