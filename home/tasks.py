from __future__ import absolute_import
from celery import shared_task
import redis

__all__ = ['add, mul, xsum']

rc = redis.StrictRedis(host='localhost', port=6379, db=0)



@shared_task
def defer_request():
    rc.set('hello', 'sup')
    print 'abc'
