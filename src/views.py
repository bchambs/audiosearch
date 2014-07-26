import ast
import json
import logging
import tasks

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext, loader, Context

import services
import src.util as util
from audiosearch.redis import client as RC
from audiosearch.config import DEBUG_TOOLBAR
cache = {}

def index(request):
    context = Context({})

    return render(request, 'index.html', context)


def artist(request, *args, **kwargs):
    artist = kwargs['artist']
    

    ###############################################
    context = Context({
        'name': artist,
        'debug': kwargs.get('debug'),
    })

    resources = RC.hgetall(artist)

    if 'profile' in resources:
        context['profile'] = ast.literal_eval(resources['profile'])
    else:
        tasks.call.delay(services.ArtistProfile(artist))

    if 'songs' in resources:
        songs = ast.literal_eval(resources['songs'])
        context['songs'] = util.page_resource(None, songs)
    else:
        tasks.call.delay(services.ArtistSongs(artist))

    if 'similar_artists' in resources:
        similar_artists = ast.literal_eval(resources['similar_artists'])
        context['similar_artists'] = util.page_resource(None, similar_artists)
    else:
        tasks.call.delay(services.SimilarArtists(artist))

    if 'similar_songs' in resources:
        similar_songs = ast.literal_eval(resources['similar_songs'])
        context['similar_songs'] = util.page_resource(None, similar_songs)
    else:
        tasks.call.delay(services.SimilarSongs(artist, "artist"))

    if artist not in cache:
        cache[artist] = {}  
    cc = cache[artist]
    if 'context' in cc:
        wrap = {'context': context.dicts[1]}
        cc['context'].update(wrap)
    else:
        cc['context'] = context.dicts[1]


    return render(request, "artist.html", context)


def similar(request, *args, **kwargs):
    artist = kwargs['artist']
    song = kwargs.get('song')
    resource_type = request.GET.get('type')
    page = request.GET.get('page')
    page_type = "song" if song else "artist"
    resource_id = song if song else artist

    context = Context({
        'name': resource_id,
        'debug': kwargs.get('debug'),
    })

    resources = RC.hgetall(resource_id)

    if 'profile' in resources:
        context['profile'] = ast.literal_eval(resources['profile'])
    else:
        service = services.SongProfile(resource_id) if song else services.ArtistProfile(resource_id)
        tasks.call.delay(service)

    if resource_type == "artists":
        if 'similar_artists' in resources:
            similar_artists = ast.literal_eval(resources['similar_artists'])
            context['similar_artists'] = util.page_resource(page, similar_artists)
        else:
            tasks.call.delay(services.SimilarArtists(resource_id))

    elif resource_type == "songs":
        if 'similar_songs' in resources:
            similar_songs = ast.literal_eval(resources['similar_songs'])
            context['similar_songs'] = util.page_resource(page, similar_songs)
        else:
            tasks.call.delay(services.SimilarSongs(resource_id, page_type))

    if artist not in cache:
        cache[artist] = {}  
    cc = cache[artist]
    if 'context' in cc:
        wrap = {'context': context.dicts[1]}
        cc['context'].update(wrap)
    else:
        cc['context'] = context.dicts[1]

    return render(request, "similar.html", context)


# HTTP 500
def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


def debug(request):
    id_ = request.GET.get('q')
    url = "/music/" + id_

    print dir(request)
    print
    print request.get_full_path()
    print request.path
    print request.path_info

    if id_ in cache:
        pass
        # util.print_cache(cache[id_])
        # print type(cache[id_]['context']['similar_artists']['data'][0])
        # print cache[id_]['context']['similar_artists']['data'][0]['name']
    else:
        print "not cached"

    return redirect(url)

"""
-------------------------------------
Functions for handling ASYNC requests
-------------------------------------
"""

# check cache, if hit return json else return pending
def retrieve_resource(request):
    id_ = request.GET.get('q')
    rtype = request.GET.get('rtype')
    page = request.GET.get('page')

    if cfg.REDIS_DEBUG:
        RC.delete(id_)

    context = {}
    resource_string = RC.hget(id_, rtype)

    if resource_string:
        resource = ast.literal_eval(resource_string)

        if rtype == "profile":
            context[rtype] = resource
        else:
            context = util.page_resource_async(page, resource, rtype)

        context['q'] = id_
        context['status'] = "ready"

    else:
        context['status'] = "pending"

    if cfg.VIEW_DEBUG and context['status'] == "ready":
        util.inspect_context(context)

    return HttpResponse(json.dumps(context), content_type="application/json")



def clear_resource(request):
    resource_id = request.GET.get('id')
    hit = RC.delete(resource_id)

    if hit: print "Removed from Redis: %s" %(resource_id)
    else: print "Resource not in Redis: %s" %(resource_id)

    return HttpResponse(json.dumps({}), content_type="application/json")


def debug_template(request):
    util.print_cache(cache)

    return HttpResponse(json.dumps({}), content_type="application/json")
