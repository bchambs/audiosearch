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

    for package in packages:
        raw = ENConsumer.consume(package, snooze, limit)

        if raw[0] == 'ready':
            resource = package.trim(raw)
            pipe = RC.pipeline()
            pipe.hset(id_, 'status', {package.REDIS_ID: 'ready'})
            pipe.hset(id_, package.REDIS_ID, resource[1])
            pipe.execute()
        else:
            client.pipe.hset(id_, 'status', raw[0])

        debug(s=raw[0], d=raw[1], keys=True)
