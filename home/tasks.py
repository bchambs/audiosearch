from __future__ import absolute_import
from json import JSONEncoder

from celery import shared_task

from audiosearch.redis import client as RC, EXPIRE_TIME
from home.util import process_artist

# call Echo Nest, encode json to dict, store in redis as <id, json_str>
@shared_task
def call_API(package):
    result = package.consume()

    # reduce json size if artist
    if package.ctype == 'artist' and result['status'] == 'ready':
        process_artist(result)

    encoded_result = JSONEncoder().encode(result)
    RC.set(package.id, encoded_result, ex=EXPIRE_TIME)
