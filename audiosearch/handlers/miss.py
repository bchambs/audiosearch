from __future__ import absolute_import

from audiosearch import tasks


def get_echo_nest_data(key, ttl, service_builder):
    service = service_builder()
    tasks.call_echo_nest.delay(key, ttl, service, service.dependencies)

