import ast
import json
import logging
import urllib

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template import RequestContext, loader, Context

from src import services, utils, tasks
from audiosearch.redis import client as RC
from audiosearch.config import DEBUG_TOOLBAR


def index(request, **kwargs):
    context = Context({})

    return render(request, 'index.html', context)


def artist(request, **kwargs):
    prefix = "artist:"
    resource_id = urllib.unquote_plus(kwargs['artist'])
    resource = prefix + resource_id

    context = Context({
        'resource_id': resource_id,
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_id),
        'songs': services.ArtistSongs(resource_id),
        'similar_artists': services.SimilarArtists(resource_id),
        'similar_songs': services.SimilarSongs(resource_id, "artist"),
    }

    content = utils.generate_content(resource, service_map)
    context.update(content)

    return render(request, "artist.html", context)


def similar(request, **kwargs):
    artist = urllib.unquote_plus(kwargs['artist'])
    song = kwargs.get('song')
    page = request.GET.get('page')
    display_type = request.GET.get('type')
    resource_type = "song" if song else "artist"

    if song:
        song = urllib.unquote_plus(song)
        prefix = "song:"
        resource_id = song

        service_map = {
            'profile': services.SongProfile(artist, resource_id),
        }
    else:
        prefix = "artist:"
        resource_id = artist

        service_map = {
            'profile': services.ArtistProfile(resource_id),
        }

    if not display_type or display_type == "songs":
        service_map['similar_songs'] = services.SimilarSongs(resource_id, resource_type, artist_id=artist, song_id=song)
    
    if not display_type or display_type == "artists":
        service_map['similar_artists'] = services.SimilarArtists(artist)

    resource = prefix + resource_id

    context = Context({
        'resource_id': resource_id,
        'debug': kwargs.get('debug'),
    })

    content = utils.generate_content(resource, service_map, page=page)
    context.update(content)

    # add all content items to context['content']. in templates, iterate over this so i dont have to type everything 3 times hehehhehehehehehheheheh

    return render(request, "similar.html", context)


def artist_songs(request, **kwargs):
    artist = kwargs['artist']
    page = request.GET.get('page')
    context = Context({
        'dir_name': urllib.unquote_plus(artist),
        'debug': kwargs.get('debug'),
    })

    data_map = {
        'profile': services.ArtistProfile(artist),
        'songs': services.ArtistSongs(artist),
    }

    content = utils.generate_content(artist, data_map, page=page)
    context.update(content)

    return render(request, "artist-songs.html", context)


def search(request, **kwargs):
    q = request.GET.get('q')
    qstr = "search:" + q
    page = request.GET.get('page')
    page_type = request.GET.get('type')

    context = Context({
        'dir_name': urllib.unquote_plus(q),
        'type': page_type,
        'debug': kwargs.get('debug'),
    })

    data_map = {
        'artists': services.SearchArtists(q),
        'songs': services.SearchSongs(q),
    }

    content = utils.generate_content(qstr, data_map, page=page)
    context.update(content)

    return render(request, "search.html", context)


def song(request, **kwargs):
    print "in song view"
    prefix = "song:"
    artist_id = urllib.unquote_plus(kwargs['artist'])
    resource_id = urllib.unquote_plus(kwargs['song'])
    resource = prefix + resource_id

    context = Context({
        'dir_artist': artist_id,
        'dir_song': resource_id,
        'debug': kwargs.get('debug'),
    })

    data_map = {
        'songs': services.SearchSongs(artist_id, resource_id, for_id=True),
        'similar_artists': services.SimilarArtists(artist),
        'similar_songs': services.SimilarSongs(resource_id, "song", artist_id, song_id=resource_id),
        'profile': services.SongProfile(artist_id, resource_id),
    }

    content = utils.generate_content(resource, data_map)
    context.update(content)

    if 'profile' in content:
        print content['profile'].keys()

    return render(request, "song.html", context)


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
    # utils.print_cache(utils.local_cache)

    return HttpResponse(json.dumps({}), content_type="application/json")
