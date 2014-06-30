from __future__ import absolute_import
from json import JSONEncoder

from celery import shared_task

from home.call_consumer import ENConsumer
from audiosearch.redis import client as RC, EXPIRE_TIME

# TODO: move this somewhere
snooze = 2
limit = 5

@shared_task
def call_service(id_, packages):
    """
    Call Echo Nest, trim json result, encode json to dict, store in redis as <id, json_str>
    """
    result = {}

    for package in packages:
        resource = ENConsumer.consume(package, snooze, limit)

        if resource['status'] == "ready":
            result.update(package.trim(resource))
        else:
            encoded_result = JSONEncoder().encode(resource)
            RC.set(id_, encoded_result, ex=EXPIRE_TIME)
            return

    result['status'] = "ready"
    encoded_result = JSONEncoder().encode(result)
    RC.set(id_, encoded_result, ex=EXPIRE_TIME)

