from __future__ import absolute_import
import logging
import sys

from celery import shared_task

import audiosearch.config as cfg
from audiosearch.redis import client as RC
from src.consumer import ENConsumer
from src.services import ENCallFailure


@shared_task
def call(package):
    """
    Consume Echo Nest service according to package spec.  Store result in Redis.
    """

    try:
        echo_nest_resource = ENConsumer.consume(package)
        resource = package.trim(echo_nest_resource)
        pipe = RC.pipeline()

        pipe.hset(package.id_, "status", {package.REDIS_KEY: "ready"})
        pipe.hset(package.id_, "type", package.TYPE_) # REDO
        pipe.hset(package.id_, package.REDIS_KEY, resource)
        pipe.expire(package.id_, package.ttl)
        pipe.execute()

    except ENCallFailure as err_msg:
        RC.hset(package.id_, "status", err_msg)

        if package.debug:
            log.warning("Call failed: %s" % err_msg)

