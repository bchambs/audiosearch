import ast
import json
import logging
import tasks

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext, loader, Context

import audiosearch.config as cfg
import services
import src.util as util
from audiosearch.redis import client as RC


log = logging.getLogger("audiosearch")

"""
---------------------------
Functions for serving pages
---------------------------
"""

def index(request):
    context = Context({})

    return render(request, 'index.html', context)


def search(request):
    """
    /search/
    """

    # obtain query params
    display_type = request.GET.get('type', "all").lower()
    search_name = request.GET.get('q')
    page = request.GET.get('page')

    # redirect on malformed request
    if search_name:
        search_name = search_name.lower()
    else:
        return HttpResponseRedirect('/')

    context = Context({
        'q': search_name,
        'type': display_type,
        'page': page,
    })

    if cfg.REDIS_DEBUG:
        RC.delete(search_name)

    resource = RC.hgetall(search_name)

    # branch on @type, add paged results to context, call celery on missing resources
    if display_type == "artists":
        if 'artists' in resource:
            artists = ast.literal_eval(resource['artists'])
            context['paged_type'] = util.page_resource(page, artists)
        else:
            tasks.call.delay(services.ArtistSearch(search_name))
            context['artists_pending'] = True

    elif display_type == "songs":
        if 'songs' in resource:
            songs = ast.literal_eval(resource['songs'])
            context['paged_type'] = util.page_resource(page, songs)
        else:
            tasks.call.delay(services.SongSearch(search_name))
            context['songs_pending'] = True
    else:
        if 'artists' in resource:
            artists = ast.literal_eval(resource['artists'])
            context['paged_artists'] = util.page_resource(page, artists)
        else:
            tasks.call.delay(services.ArtistSearch(search_name))
            context['artists_pending'] = True

        if 'songs' in resource:
            songs = ast.literal_eval(resource['songs'])
            context['paged_songs'] = util.page_resource(page, songs)
        else:
            tasks.call.delay(services.SongSearch(search_name))
            context['songs_pending'] = True

    if cfg.VIEW_DEBUG:
        util.inspect_context(context)

    return render(request, 'search.html', context)


def artist(request, artist):
    id_ = request.GET.get('q')
    context = Context({
        'q': id_
    })

    resources = RC.hgetall(id_)

    if 'profile' in resources:
        context['profile'] = ast.literal_eval(resources['profile'])
    else:
        tasks.call.delay(services.ArtistProfile(id_))

    if 'songs' in resources:
        songs = ast.literal_eval(resources['songs'])
        context['songs'] = util.page_resource(None, songs)
    else:
        tasks.call.delay(services.ArtistSongs(id_))

    if 'similar_artists' in resources:
        similar_artists = ast.literal_eval(resources['similar_artists'])
        context['similar_artists'] = util.page_resource(None, similar_artists)
    else:
        tasks.call.delay(services.SimilarArtists(id_))

    if 'similar_songs' in resources:
        similar_songs = ast.literal_eval(resources['similar_songs'])
        context['similar_songs'] = util.page_resource(None, similar_songs)
    else:
        tasks.call.delay(services.SimilarSongs(id_))

    if cfg.VIEW_DEBUG:
        util.inspect_context(context)

    return render(request, "artist.html", context)


def artist_similar(request):
    id_ = request.GET.get('q')
    page = request.GET.get('page')
    context = Context({
        'q': id_,
        'page': page,
    })

    if cfg.REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hget(id_, 'similar')

    if resource:
        similar = ast.literal_eval(resource)
        context['similar'] = util.page_resource(page, similar)
    else:
        tasks.call.delay(services.ArtistSimilar(id_))
        tasks.call.delay(services.ArtistProfile(id_))
        tasks.call.delay(services.ArtistSongs(id_))

    if cfg.VIEW_DEBUG:
        util.inspect_context(context)

    return render(request, "artist-similar.html", context)


def artist_songs(request):
    id_ = request.GET.get('q')
    page = request.GET.get('page')
    context = Context({
        'q': id_,
        'page': page,
    })

    if cfg.REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hget(id_, 'songs')

    if resource:
        songs = ast.literal_eval(resource)
        context['songs'] = util.page_resource(page, songs)
    else:
        tasks.call.delay(services.ArtistSongs(id_))
        tasks.call.delay(services.ArtistSimilar(id_))
        tasks.call.delay(services.ArtistProfile(id_))

    if cfg.VIEW_DEBUG:
        util.inspect_context(context)

    return render(request, "artist-songs.html", context)


def song_profile(request):
    id_ = request.GET.get('q')
    page = request.GET.get('page')

    context = Context({
        'q': id_
    })

    if cfg.REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hgetall(id_)

    if 'similar_songs' in resource:
        songs = ast.literal_eval(resource['similar_songs'])
        context['similar_songs'] = util.page_resource(page, songs)
    else:
        tasks.call.delay(services.SimilarSongs(id_))

    if cfg.VIEW_DEBUG:
        util.inspect_context(context)

    return render(request, "song-profile.html", context)


# HTTP 500
def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


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


