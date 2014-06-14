from __future__ import absolute_import

from celery import shared_task
import .redis_client

__all__ = ['add, mul, xsum']


@shared_task
def defer_request():
    pass


@shared_task
def xsum(numbers):
    return sum(numbers)