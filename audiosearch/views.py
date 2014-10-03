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


def search(request, querydict, page, **kwargs):
    return render(request, 'artist-home.html', Context({}))


@stdout_gap
def music_home(request, querydict, page, **kwargs):
    context = {}
    top = artist.Top_Hottt()

    if top.key in Cache:
        datawrap = Cache.fetch(top.key, page)
        context[top] = datawrap
    else:
        # get.delay(top)
        get(top)
        context[top] = None

    packaged_context = processors.prepare(context, page)
    return render(request, 'music-home-base.html', Context(packaged_context))


def song_home(request, querydict, page, **kwargs):
    return render(request, 'song-home.html', Context({}))


@stdout_gap
def artist_home(request, querydict, page, **kwargs):
    artist_name = kwargs.get('artist')
    if not artist_name:
        return redirect(music_home)

    context = {}
    resources = [
        artist.Profile(artist_name),
        # artist.Songs(artist_name),
    ]

    for resource in resources:
        if resource.key in Cache:
            datawrap = Cache.fetch(resource.key, page)
            context[resource] = datawrap
        else:
            # get.delay(resource)
            get(resource)
            context[resource] = None

    packaged_context = processors.prepare(context, page)
    packaged_context['artist_name'] = artist_name.title()
    packaged_context['RCKEY'] = artist.Profile(artist_name).key
    return render(request, 'artist-home-base.html', Context(packaged_context))


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

    except (AttributeError, KeyError, TypeError):
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


def ajax_clear(request, querydict, page, **kwargs):
    try:
        key = querydict.pop('RCKEY')
    except KeyError:
        hit = False
        key = "NO KEY"
    else:
        hit = Cache.delete(key)

    msg = "Removed: {}".format(key) if hit else "Not found: {}".format(key)
    print "\n{}\n".format(msg)

    return HttpResponse(json.dumps({}), content_type="application/json")


@shared_task(base=tasks.SharedConnection, default_retry_delay=2, max_retries=5)
def get(resource):
    service_params = resource.get_service_params()
    try:
        response = echonest.call(resource.group, resource.method, service_params)
        raw_data = echonest.parse(response, resource.response_key)
        echodata = resource.clean(raw_data)

        if type(echodata) is list:
            Cache.set_list(resource.key, echodata)
        elif type(echodata) is dict:
            Cache.set_hash(resource.key, echodata)
        else:
            Cache.set_failed(resource.key)
    except (APIConnectionError, APIResponseError) as e:
        Cache.set_failed(resource.key)
    except RateLimitError as e:
        get.retry(exc=e)
