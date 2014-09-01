from __future__ import absolute_import

from audiosearch import tasks


def get_echonest_data(key, service_builder, ttl):
    service = service_builder()
    tasks.call_echo_nest.delay(key, ttl, service, service.dependencies)

