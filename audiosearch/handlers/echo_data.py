from __future__ import absolute_import

from audiosearch import tasks
from audiosearch.models.service import ServiceFactory


def get_echo_data(key, category, content, params):
    service = ServiceFactory(category, content, params)
    tasks.call_api.delay(key, service)


