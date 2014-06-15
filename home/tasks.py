from __future__ import absolute_import
from celery import shared_task
from pyechonest.util import EchoNestAPIError
from pyechonest import config, artist, song
from time import sleep

import json
import redis

__all__ = ['add, mul, xsum']
config.ECHO_NEST_API_KEY='QZQG43T7640VIF4FN'
rc = redis.StrictRedis(host='localhost', port=6379, db=0)

@shared_task
def call_API(query, ignore_result=True):
    ready = False
    snooze = 2

    while not ready:
        sleep(4)
        try:
            # get artist
            artist_ = artist.Artist(query, buckets=['biographies', 'hotttnesss', 'images', 'terms'])
            
            # create dict
            context = {
                'artist_name': artist_.name
            }

            # return if in cache
            if rc.exists(query):
                print 'hash exists'
                return 

            # store
            else:
                # serialize to json
                js = json.JSONEncoder().encode(context)
                rc.lpush(query, js)
                print 'storing: %s, %s' % (query, rc.type(query))

            ready = True

        except EchoNestAPIError:
            print 'snoozing'
            sleep(snooze)


@shared_task
def get_data(query):
    x = 0

    print '\tin get_data for: %s' % query
    while not rc.exists(query) and x < 5:
        print '\tdne snooze'
        sleep (2)
        x += 1

    temp = rc.blpop(query,timeout=6)
    print 'redis complete'

    return temp