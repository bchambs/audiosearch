from __future__ import absolute_import
import json

from celery import shared_task
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import Context

# from audiosearch.models import factory
from audiosearch import Cache
from audiosearch.conf import tasks
from audiosearch.core import echonest
from audiosearch.core import processors
from audiosearch.core.exceptions import (APIConnectionError, APIResponseError, RateLimitError)
from audiosearch.models import artist
from audiosearch.utils.decorators import stdout_gap


@shared_task(base=tasks.SharedConnection, default_retry_delay=2, max_retries=5)
def get(resource):
    try:
        echo_response = echonest.call(resource.group, resource.method, 
                                    resource.params)
        echodata = echonest.parse(echo_response, resource.response_key)

        if type(echodata) is list:
            Cache.setlist(resource.key, echodata)
        elif type(echodata) is dict:
            Cache.sethash(resource.key, echodata)
        else:
            Cache.set_failed(resource.key)
    except (APIConnectionError, APIResponseError) as e:
        Cache.set_failed(resource.key)
    except RateLimitError as e:
        get.retry(exc=e)


@stdout_gap
def music_home(request, qparams, page, **kwargs):
    context = {}
    top = artist.Top_Hottt()

    Cache.delete(top.key)

    if top.key in Cache:
        print 'hit'
        data_pair = Cache.fetch(top.key)
        context[top] = data_pair
    else:
        print 'miss'
        get(top)
        context[top] = None

    packaged_context = processors.prepare(context, page)
    return render(request, 'music-home.html', Context(packaged_context))


def ajax_retrieve(request, qparams, page, **kwargs):
    print 'in ajax'
    print kwargs.keys()

    try:
        resource = kwargs.pop('resource')
    except KeyError as e:
        print e
        return HttpResponse(json.dumps({'status': 'failed'}),
                            content_type="application/json")

    print resource.key
    context = {}
    if resource.key in Cache:
        data_pair = Cache.fetch(resource.key, page)
        context[resource] = data_pair
    else:
        context[resource] = None

    packaged_context = processors.prepare(request, context, page)
    return HttpResponse(json.dumps(packaged_context), 
                        content_type="application/json")


# def ajax_retrieve(request, qparams, page, **kwargs):
#     failed = dict(status='failed')
#     return HttpResponse(json.dumps(failed), content_type="application/json")

#     try:
#         group = kwargs.pop('group')
#         method = kwargs.pop('method')
#     except KeyError:
#         failed = dict(status='failed')
#         return HttpResponse(json.dumps(failed), content_type="application/json")

#     context = {}
#     resource = factory.Resource(group, method, qparams)
#     if not resource:
#         failed = dict(status='failed')
#         return HttpResponse(json.dumps(failed), content_type="application/json")

#     if resource.key in Cache:
#         data_pair = Cache.fetch(resource.key, page)
#         context[resource] = data_pair
#     else:
#         context[resource] = None

#     packaged_context = processors.prepare(request, context, page)
#     return HttpResponse(json.dumps(packaged_context), 
#                         content_type="application/json")
