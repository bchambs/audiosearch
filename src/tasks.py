from celery import shared_task

from audiosearch.redis import client as cache
from consumer import ENConsumer
import services


@shared_task
def acquire_resource(resource_id, content_key, service):
    if ':' not in resource_id:print "\nSTORED AN INVALID resource_id" * 3

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

        print "\nSTORING, %s:%s\n" %(resource_id, content_key)

    except services.EchoNestServiceFailure as err_msg:
        content_struct = {
            'status': "failed",
            'error_message': str(err_msg),
        }
        pipe.hset(resource_id, content_key, content_struct)

        print "%s:%s__%s__ failed: %s" % (resource_id, content_key, str(service), err_msg)

    pipe.expire(resource_id, service.ttl)
    pipe.execute()



