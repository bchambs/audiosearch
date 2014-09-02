from __future__ import absolute_import

from audiosearch import tasks


def get_echo_data(resource):
    key = resource.key
    ttl = resource.ttl
    build = resource.build_service

    def _queue_api_call():
        service = build()
        return tasks.api_get_data.delay(key, ttl, service, service.dependencies)

    return _queue_api_call

