import logging

from celery import shared_task

from audiosearch.redis import client as cache
from consumer import ENConsumer
import services
import utils


redis_logger = logging.getLogger("redis_logger")


@shared_task
def log_dbsize():
    key_count = cache.dbsize()
    redis_logger.info("KEY_COUNT: %s" %(key_count))




@shared_task
def examine_cache():
    pass




@shared_task
def acquire_resource(resource_id, content_key, service):
    if ':' not in resource_id:
        error = "Malformed resource_id received in acquire_resource."
        redis_logger.error(utils.clm(error, resource_id, content_key, service))

    pipe = cache.pipeline()

    try:
        if service.dependency:
            intermediate = ENConsumer.consume(service.dependency)
            service.build(intermediate)

        echo_nest_response = ENConsumer.consume(service)
        content = service.trim(echo_nest_response)

        content_struct = {
            'status': "complete",
            'data': content,
        }

        pipe.hset(resource_id, content_key, content_struct)

    except services.EchoNestServiceFailure as err_msg:
        content_struct = {
            'status': "failed",
            'error_message': str(err_msg),
        }
        pipe.hset(resource_id, content_key, content_struct)

        redis_logger.error(utils.clm(err_msg, resource_id, content_key, service))
        
    except services.EmptyServiceResponse:
        content_struct = {
            'status': "empty",
            'error_message': "None.",
        }
        pipe.hset(resource_id, content_key, content_struct)

    pipe.expire(resource_id, service.ttl)
    pipe.execute()


    


