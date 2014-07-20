from __future__ import absolute_import
import logging
import sys

from celery import shared_task

import audiosearch.config as cfg
from audiosearch.redis import client as RC
from src.consumer import ENConsumer


@shared_task
def call(package):
    """
    Consume Echo Nest service according to package spec.  Store result in Redis.
    """

    raw = ENConsumer.consume(package, cfg.CALL_SNOOZE, cfg.CALL_TIMEOUT)

    if raw[0] == "ready":
        resource = package.trim(raw[1])
        pipe = RC.pipeline()

        pipe.hset(package.id_, "status", {package.REDIS_ID: "ready"})
        pipe.hset(package.id_, package.REDIS_ID, resource)
        pipe.expire(package.id_, cfg.REDIS_TTL)
        pipe.execute()
    else:
        RC.hset(package.id_, "status", raw[0])

