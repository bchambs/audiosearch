from __future__ import absolute_import

from celery import shared_task

from audiosearch.models.service import consume, ServiceFailureError


@shared_task
def call_api(key, service):
    if service.dependency:
        try:
            intermediate = consume(service.dependency)
        except ServiceFailureError:
            return
        req_fields = service.dependency.build(intermediate)
        service.payload.update(req_fields)




    # if not continue_task: return
    # print 3

    # if dependencies:
    #     try:
    #         _fulfill_dependencies(service, dependencies)
    #     except EmptyResponseError:
    #         client.establish_failed(key, messages.NO_DATA)
    #         return False
    #     except DependencyError:
    #         client.establish_failed(key, messages.CONTENT_CREATION_FAIL)
    #         logger.exception(key)
    #         return False
    #     except ServiceError as e:
    #         client.establish_failed(key, repr(e))
    #         logger.exception("%s: %s" %(key, repr(e)))
    #         return False
    # print 4

    # try:
    #     echo_nest_response = consume(service)
    # except EmptyResponseError:
    #     client.establish_failed(key, messages.NO_DATA)
    # except ServiceError as e:
    #     logger.exception("%s: %s" %(key, repr(e)))
    #     client.establish_failed(key, str(e))
    # else:
    #     print 5

    #     try:
    #         data = service.process(echo_nest_response)
    #     except AttributeError:
    #         data = echo_nest_response
    #     print 6
        
    #     client.store(key, data, ttl)
    #     print 7
    pass



