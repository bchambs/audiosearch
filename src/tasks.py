from __future__ import absolute_import
import logging
import sys

from celery import shared_task

from audiosearch.redis import client as RC
from src.consumer import ENConsumer
from src.services import ENCallFailure


@shared_task
def call(package):

    try:
        echo_nest_resource = ENConsumer.consume(package)
        resource = package.trim(echo_nest_resource)
        pipe = RC.pipeline()

        # pipe.hset(package.id_, "status", {package.REDIS_KEY: "ready"})
        # pipe.hset(package.id_, "type", package.TYPE_) # REDO
        pipe.hset(package.call_id, package.REDIS_KEY, resource)
        pipe.expire(package.call_id, package.ttl)
        pipe.execute()

    except ENCallFailure as err_msg:
        RC.hset(package.call_id, "error_msg", err_msg)  # this overwrites
        print "%s failed: %s" % (str(package), err_msg)


