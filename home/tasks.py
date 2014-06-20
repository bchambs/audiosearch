from __future__ import absolute_import
from celery import shared_task
from time import sleep
from audiosearch.redis import client as RC
from home.util import debug_title

import json

# call Echo Nest, encode json to dict, store in redis as <id, dict>
@shared_task
def call_API(package, ignore_result=True):
    pass
    # result = package.consume()
    # enc_result = json.JSONEncoder().encode(result)
    # RC.lpush(package.id, enc_result)
    # debug_title('stored woooo')


@shared_task
def get_data(query, ignore_result=True):
    x = 0

    print '\tin get_data for: %s' % query
    while not rc.exists(query) and x < 5:
        print '\tdne snooze'
        sleep (2)
        x += 1

    temp = rc.blpop(query,timeout=6)
    print 'redis complete'

    return temp