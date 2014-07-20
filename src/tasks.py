from __future__ import absolute_import
import logging
import sys

from celery import shared_task

from src.call_consumer import ENConsumer
# from audiosearch.redis import client as RC, EXPIRE_TIME
from audiosearch.redis import client as RC
from audiosearch.settings import REDIS_KEY_TTL
from src.util import debug, debug_subtitle


# TODO: move this somewhere
SNOOZE = 2
LIMIT = 5

@shared_task
def call(package, key_ttl=None):
    """
    Consume Echo Nest service according to package spec.  Store result in Redis.
    """

    raw = ENConsumer.consume(package, SNOOZE, LIMIT)

    if raw[0] == "ready":
        ttl = key_ttl or REDIS_KEY_TTL
        resource = package.trim(raw[1])
        pipe = RC.pipeline()

        pipe.hset(package.id_, "status", {package.REDIS_ID: "ready"})
        pipe.hset(package.id_, package.REDIS_ID, resource)
        pipe.expire(package.id_, ttl)
        pipe.execute()
    else:
        RC.hset(package.id_, "status", raw[0])

