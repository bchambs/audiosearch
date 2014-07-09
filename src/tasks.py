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
def call_service(package):
    """
    Consume Echo Nest service according to package spec.  Store result in Redis.
    """

    raw = ENConsumer.consume(package, SNOOZE, LIMIT)

    if raw[0] == 'ready':
        resource = package.trim(raw[1])
        pipe = RC.pipeline()
        pipe.hset(package.id_, 'status', {package.REDIS_ID: 'ready'})
        pipe.hset(package.id_, package.REDIS_ID, resource)
        pipe.execute()

        # logging.info(' ')
        # logging.info('=========================')
        # logging.info(len(resource))
        # logging.info('=========================')
        # logging.info(' ')

        # if resource:
        #     logging.info('=========================')
        #     logging.info(package.REDIS_ID)
        #     if isinstance(resource, dict):
        #         for k in resource.keys():
        #             logging.info(k)
        #     elif isinstance(resource, list):
        #         logging.info(resource[0])
        #     else:
        #         logging.info("INVALID RESOURCE")
        #     logging.info('=========================')

    else:
        RC.hset(package.id_, 'status', raw[0])

