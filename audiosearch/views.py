from __future__ import absolute_import
import json

from celery import shared_task
from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import Context

from audiosearch import Cache
from audiosearch.conf import tasks
from audiosearch.core import echonest
from audiosearch.core.exceptions import (APIConnectionError, APIResponseError, 
                                        RateLimitError)
from audiosearch.models import artist
from audiosearch.utils.decorators import stdout_gap


@shared_task(base=tasks.SharedConnection, default_retry_delay=2, max_retries=5)
def get(resource, page=None):
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
        print e
        Cache.set_failed(resource.key)
    except RateLimitError as e:
        get.retry(exc=e)

def process_miss(resource):
    async_params = {
        'div_id': resource.method,
        'group': resource.group,
        'method': resource.method,
        'name': resource.name,
        'title': resource.description,
    }
    return async_params

def process_hit(resource, data):
    template_dict = {
        'div_id': resource.method,
        'title': resource.description,
        'resource_data': data,
    }
    return template_dict

# 'page': page,
#         'has_next': end < size,
#         'has_previous': start > size,

@stdout_gap
def music_home(request, qparams, **kwargs):
    top = artist.TopHottt()
    context = {}

    if top.key in Cache:
        print 'hit'
        top_data = Cache.fetch(top.key)
        context[top.method] = process_hit(top, top_data)
    else:
        print 'miss'
        get(top)
        context[top.method] = process_miss(top)

    print context['top_hottt']

    return render(request, 'music-home.html', Context(context))



def ajax_retrieve_content(request, GET, **kwargs):
    context = dict(status='failed')
    return HttpResponse(json.dumps(context), content_type="application/json")
