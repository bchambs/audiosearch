from __future__ import absolute_import
from json import JSONEncoder

from celery import shared_task

from audiosearch.redis import client as RC, EXPIRE_TIME
from home.util import process_artist

# call Echo Nest, encode json to dict, store in redis as <id, json_str>
@shared_task
def call_API(*packages):
    result = {}

    for package in packages:
        temp_result = package.consume()

        # reduce json size if artist
        # TODO: this work needs to be done outside of the task
        if package.ctype == 'artist' and temp_result['status'] == 'ready':
            process_artist(temp_result)

        result.update(temp_result)
    
    encoded_result = JSONEncoder().encode(result)
    RC.set(package.id, encoded_result, ex=EXPIRE_TIME)
