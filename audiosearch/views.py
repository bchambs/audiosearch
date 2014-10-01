from __future__ import absolute_import
import json

from celery import shared_task
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import Context

from audiosearch import Cache
from audiosearch import models
from audiosearch.conf import tasks
from audiosearch.core import echonest
from audiosearch.core import processors
from audiosearch.core.exceptions import (APIConnectionError, APIResponseError, RateLimitError)
from audiosearch.models import artist
from audiosearch.utils.decorators import stdout_gap


@shared_task(base=tasks.SharedConnection, default_retry_delay=2, max_retries=5)
def get(resource):
    params = resource.get_service_params()
    try:
        response = echonest.call(resource.group, resource.method, params)
        echodata = echonest.parse(response, resource.response_key)

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


# @stdout_gap
def music_home(request, querydict, page, **kwargs):
    context = {}
    # top = artist.Profile('led zeppelin')
    top = artist.Top_Hottt()

    # Cache.delete(top.key)

    if top.key in Cache:
        datawrap = Cache.fetch(top.key, page)
        context[top] = datawrap
    else:
        get(top)
        context[top] = None

    packaged_context = processors.prepare(context, page)
    return render(request, 'music-home.html', Context(packaged_context))


@stdout_gap
def ajax_retrieve(request, querydict, page, **kwargs):
    try:
        # Build resource from kwargs / scheme
        group = kwargs.pop('group')
        method = kwargs.pop('method')
        
        # Load relevant class obj from `models` module
        target = vars(models).get(group)
        klass = getattr(target, method.title())
        
        # Exec alt constructor with scheme dict
        resource = klass.from_scheme(**querydict)

    except (AttributeError, KeyError, TypeError) as e:
        print "ajax resource init error"
        print e
        print
        # Construction failed for some reason; retrieve will never succeed
        failed = {'status':'failed'}
        return HttpResponse(json.dumps(failed), content_type="application/json")

    if resource.key in Cache:
        datawrap = Cache.fetch(resource.key, page)
        resource_package = (resource, datawrap)
    else:
        resource_package = (resource, None)

    packaged_response = processors.prepare_async(request, resource_package, page)
    return HttpResponse(json.dumps(packaged_response), 
                        content_type="application/json")
