from __future__ import absolute_import
from celery import shared_task
from time import sleep
from audiosearch.redis import client as RC
from home.util import debug_title, debug
from home.models import ENCall, AudiosearchConstants as AC

import json

# call Echo Nest, encode json to dict, store in redis as <id, json_str>
@shared_task
def call_API(request_id, call_type, method):
    package = ENCall(call_type, method)
    package.build(request_id, bucket=AC.ARTIST_PROFILE_B)
    result = package.consume()

    enc_result = json.JSONEncoder().encode(result)
    RC.set(request_id, enc_result)

# block until requested json is available, then return json
@shared_task
def retrieve_json(request_id):
    print '\tin retrieve_json'

    

    print '\texiting retrieve_json'
    return temp