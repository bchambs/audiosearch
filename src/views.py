import tasks
import ast
import json

from django.shortcuts import render, redirect
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from audiosearch.settings import SEARCH_RESULT_DISPLAYED, ARTIST_SONGS_DISPLAYED, SIMILAR_ARTIST_DISPLAYED, REDIS_DEBUG, MORE_RESULTS, VIEW_DEBUG
from audiosearch.redis import client as RC
from src.calls import ArtistProfile, Playlist, SimilarArtists, ArtistSearch, SongSearch, SongProfile
from src.util import page_resource, page_resource_async

"""
audiosearch conventions:
"""


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

    if REDIS_DEBUG:
        RC.delete(search_name)

    resource = RC.hgetall(search_name)

    # branch on @type, add paged results to context, call celery on missing resources
    if display_type == "artists":
        if 'artists' in resource:
            artists = ast.literal_eval(resource['artists'])
            context['paged_type'] = page_resource(page, artists)
        else:
            tasks.call_service.delay(ArtistSearch(search_name))
            context['artists_pending'] = True

    elif display_type == "songs":
        if 'songs' in resource:
            songs = ast.literal_eval(resource['songs'])
            context['paged_type'] = page_resource(page, songs)
        else:
            tasks.call_service.delay(SongSearch(search_name))
            context['songs_pending'] = True
    else:
        if 'artists' in resource:
            artists = ast.literal_eval(resource['artists'])
            context['paged_artists'] = page_resource(page, artists)
        else:
            tasks.call_service.delay(ArtistSearch(search_name))
            context['artists_pending'] = True

        if 'songs' in resource:
            songs = ast.literal_eval(resource['songs'])
            context['paged_songs'] = page_resource(page, songs)
        else:
            tasks.call_service.delay(SongSearch(search_name))
            context['songs_pending'] = True

    # print context['offset']

    return render(request, 'search.html', context)


def artist_profile(request):
    """
    /artist/
    """
    id_ = request.GET.get('q')
    context = Context({
        'q': id_
    })

    if REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hgetall(id_)

    if 'profile' in resource:
        context['profile'] = ast.literal_eval(resource['profile'])
    else:
        tasks.call_service.delay(ArtistProfile(id_))

    if 'songs' in resource:
        songs = ast.literal_eval(resource['songs'])
        context['songs'] = page_resource(None, songs)
        print len(context['songs'])
        if len (songs) > SEARCH_RESULT_DISPLAYED:
            context['more_songs'] = True
    else:
        tasks.call_service.delay(Playlist(id_))

    if 'similar' in resource:
        similar = ast.literal_eval(resource['similar'])
        context['similar'] = similar[:18]
    else:
        tasks.call_service.delay(SimilarArtists(id_))

    return render(request, "artist-profile.html", context)


def artist_similar(request):
    id_ = request.GET.get('q')
    page = request.GET.get('page')
    context = Context({
        'q': id_,
        'page': page,
    })

    if REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hget(id_, 'similar')

    if resource:
        similar = ast.literal_eval(resource)
        context['similar'] = page_resource(page, similar)
    else:
        tasks.call_service.delay(SimilarArtists(id_))
        tasks.call_service.delay(ArtistProfile(id_))
        tasks.call_service.delay(Playlist(id_))

    return render(request, "artist-similar.html", context)


def artist_songs(request):
    id_ = request.GET.get('q')
    page = request.GET.get('page')
    context = Context({
        'q': id_,
        'page': page,
    })

    if REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hget(id_, 'songs')

    if resource:
        songs = ast.literal_eval(resource)
        context['songs'] = page_resource(page, songs)
    else:
        tasks.call_service.delay(Playlist(id_))
        tasks.call_service.delay(SimilarArtists(id_))
        tasks.call_service.delay(ArtistProfile(id_))

    return render(request, "artist-songs.html", context)


def song_profile(request):
    id_ = request.GET.get('q')

    context = Context({
        'q': id_
    })

    if REDIS_DEBUG:
        RC.delete(id_)

    resource = RC.hget(id_, 'profile')

    if resource:
        context['profile'] = ast.literal_eval(resource)
    else:
        tasks.call_service.delay(SongProfile(id_))

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

    context = {}
    resource_string = RC.hget(id_, rtype)

    if resource_string:
        resource = ast.literal_eval(resource_string)

        if rtype == "profile":
            context[rtype] = resource
        else:
            context = page_resource_async(page, resource, rtype)

        context['q'] = id_
        context['status'] = "ready"

    else:
        context['status'] = "pending"

    if VIEW_DEBUG and context['status'] == "ready":
        print "in async for: %s" % rtype
        # print context.keys()

    return HttpResponse(json.dumps(context), content_type="application/json")


