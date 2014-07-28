from celery import shared_task

from audiosearch.redis import client as cache
from consumer import ENConsumer
import services


@shared_task
def call(resource, service):

    try:
        if service.dependency:
            intermediate = ENConsumer.consume(service.dependency)
            service.build(intermediate)

        echo_nest_response = ENConsumer.consume(service)
        content = service.trim(echo_nest_response)
        pipe = cache.pipeline()

        pipe.hset(resource, service.CONTENT_KEY, content)
        pipe.expire(resource, service.ttl)
        pipe.execute()

        print 'stored key: %s' % resource
        print 'stored content: %s' % service.CONTENT_KEY

    except services.ENCallFailure as err_msg:
        cache.hset(resource, "error_msg", err_msg)  # this overwrites
        print "%s failed: %s" % (str(service), err_msg)


