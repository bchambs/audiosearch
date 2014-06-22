from __future__ import absolute_import
import json

from celery import shared_task

from audiosearch.redis import client as RC, EXPIRE_TIME
from home.util import debug_title, debug

from time import sleep

# call Echo Nest, encode json to dict, store in redis as <id, json_str>
@shared_task
def call_API(package):
    if not RC.exists(package.id):
        result = package.consume()
        encoded_result = json.JSONEncoder().encode(result)
        RC.set(package.id, encoded_result, ex=EXPIRE_TIME)
