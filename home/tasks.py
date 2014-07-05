from __future__ import absolute_import
from json import JSONEncoder
from time import sleep

from celery import shared_task

from home.call_consumer import ENConsumer
from audiosearch.redis import client as RC, EXPIRE_TIME
from home.util import debug

# TODO: move this somewhere
snooze = 2
limit = 5

@shared_task
def call_service(packages):
    """
    Call Echo Nest, trim json result, encode json to dict, store in redis as <id, json_str>
    """

    for package in packages:
        raw = ENConsumer.consume(package, snooze, limit)
        sleep(5)

        if raw[0] == 'ready':
            resource = package.trim(raw[1])
            pipe = RC.pipeline()
            pipe.hset(package.id_, 'status', {package.REDIS_ID: 'ready'})
            pipe.hset(package.id_, package.REDIS_ID, resource)
            pipe.execute()
        else:
            RC.hset(package.id_, 'status', raw[0])

