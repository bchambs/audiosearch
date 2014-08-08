from celery import shared_task

from audiosearch.redis import client as cache
from consumer import ENConsumer
import services


@shared_task
def call(resource, service, content_key):

    try:
        if service.dependency:
            intermediate = ENConsumer.consume(service.dependency)
            service.build(intermediate)
            print "%s: BUILDING dependency" %(content_key)

        echo_nest_response = ENConsumer.consume(service)
        content = service.trim(echo_nest_response)
        pipe = cache.pipeline()

        #################################
        m1 = "STORING, "
        m2 = "AT, "
        banner = '\'' * len(m1)
        banner2 = '\'' * len(m2)

        print
        print banner
        print "%s %s" %(m1, resource)
        print "%s %s" %(m2, content_key)
        print banner2
        print

        if ':' not in resource:
            print
            print
            print "STORED AN INVALID RESOURCE"
            print "STORED AN INVALID RESOURCE"
            print "STORED AN INVALID RESOURCE"
            print "STORED AN INVALID RESOURCE"
            print "STORED AN INVALID RESOURCE"
            print "STORED AN INVALID RESOURCE"
            print
            print
        #################################


        pipe.hset(resource, content_key, content)
        pipe.expire(resource, service.ttl)
        pipe.execute()

        # print 'stored key: %s' % resource
        # print 'stored content: %s' % service.CONTENT_KEY

    except services.EchoNestServiceFailure as err_msg:
        cache.hset(resource, "error_msg", err_msg)  # this overwrites
        print "%s failed: %s" % (str(service), err_msg)


