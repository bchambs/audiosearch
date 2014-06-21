from __future__ import absolute_import
from celery import shared_task
from time import sleep
import json

from audiosearch.redis import client as RC
from home.util import debug_title, debug
from home.models import ENCall, AudiosearchConstants as AC


# call Echo Nest, encode json to dict, store in redis as <id, json_str>
@shared_task
def call_API(request_id, call_type, method):
    package = ENCall(call_type, method)
    package.build(request_id, bucket=AC.ARTIST_PROFILE_B)
    result = package.consume()

    enc_result = json.JSONEncoder().encode(result)
    RC.set(request_id, enc_result)

# block until requested json is available, then return json_dict
@shared_task
def retrieve_json(request_id):
    print '\tin retrieve_json'

    if not RC.exists(request_id):
        print '\tsleeping'


    json_str = RC.get(request_id)   # catch redis
    json_dict = json.loads(json_str)

    print '\texiting retrieve_json'
    return json_dict
