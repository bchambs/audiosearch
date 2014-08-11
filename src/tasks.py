from celery import shared_task

from audiosearch.redis import client as cache
from consumer import ENConsumer
import services


@shared_task
def call(resource_id, service, content_key):

    try:
        if service.dependency:
            intermediate = ENConsumer.consume(service.dependency)
            service.build(intermediate)

        echo_nest_response = ENConsumer.consume(service)
        content = service.trim(echo_nest_response)
        pipe = cache.pipeline()

        pipe.hset(resource_id, content_key, content)
        pipe.expire(resource_id, service.ttl)
        pipe.execute()

        #################################
        print
        print "STORING, %s:%s" %(resource_id, content_key)
        print

        if ':' not in resource_id:
            print
            print
            print "STORED AN INVALID resource_id"
            print "STORED AN INVALID resource_id"
            print "STORED AN INVALID resource_id"
            print "STORED AN INVALID resource_id"
            print "STORED AN INVALID resource_id"
            print "STORED AN INVALID resource_id"
            print
            print
        #################################

    except services.EchoNestServiceFailure as err_msg:
        cache.hset(resource_id, "error_msg", err_msg)  # this overwrites
        print "%s failed: %s" % (str(service), err_msg)


