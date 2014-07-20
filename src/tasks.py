from __future__ import absolute_import
import logging
import sys

from celery import shared_task

from src.call_consumer import ENConsumer
from audiosearch.redis import client as RC, EXPIRE_TIME
from src.util import debug, debug_subtitle


# TODO: move this somewhere
SNOOZE = 2
LIMIT = 5

@shared_task
def call_service(package, expire_in=None):
    """
    Consume Echo Nest service according to package spec.  Store result in Redis.
    """

    expire_in = expire_in or EXPIRE_TIME
    print expire_in
    raw = ENConsumer.consume(package, SNOOZE, LIMIT)

    if raw[0] == "ready":
        resource = package.trim(raw[1])
        pipe = RC.pipeline()
        pipe.hset(package.id_, "status", {package.REDIS_ID: "ready"})
        pipe.hset(package.id_, package.REDIS_ID, resource)
        # pipe.expire(package.id_, EXPIRE_TIME)
        pipe.expire(package.id_, expire_in)
        pipe.execute()
    else:
        RC.hset(package.id_, "status", raw[0])

