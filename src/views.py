import ast
import json
import urllib

from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context

from src import services, utils, tasks
from audiosearch.redis import client as cache
from audiosearch.config import DEBUG_TOOLBAR




def index(request, **kwargs):
    context = Context({})

    return render(request, 'index.html', context)




def search(request, **kwargs):
    prefix = "search:"
    resource_name = urllib.unquote_plus(request.GET.get('q'))
    resource_id = prefix + resource_name
    page = request.GET.get('page')
    page_type = request.GET.get('type')

    try:
        page_type = page_type.lower()
    except AttributeError:
        page_type = None

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'page_type': page_type,
        'page': page,
        'use_generic_key': True if page_type else False,
        'debug': kwargs.get('debug'),
    })

    if page_type == "artists":
        service_map = {
            'search_artists': services.SearchArtists(resource_name),
        }
    elif page_type == "songs":
        service_map = {
            'search_songs': services.SearchSongs(None, resource_name),
        }
    else:
        service_map = {
            'search_artists': services.SearchArtists(resource_name),
            'search_songs': services.SearchSongs(None, resource_name),
        }

    content = utils.generate_content(resource_id, service_map, page=page)
    if page_type == "artists" and 'search_artists' in content:
        content['content'] = content.pop('search_artists')
        content['use_content_keys'] = False

    elif page_type == "songs" and 'search_songs' in content:
        content['content'] = content.pop('search_songs')
        content['use_content_keys'] = False

    else:
        content['use_content_keys'] = True

    context.update(content)

    return render(request, "search.html", context)




def artist_summary(request, **kwargs):
    prefix = "artist:"
    resource_name = urllib.unquote_plus(kwargs['artist'])
    resource_id = prefix + resource_name

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'use_generic_key': False,
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_name),
        'songs': services.ArtistSongs(resource_name),
        'similar_artists': services.SimilarArtists(resource_name),
        'playlist': services.Playlist(resource_name),
    }

    content = utils.generate_content(resource_id, service_map)
    context.update(content)

    return render(request, "artist-summary.html", context)




def artist_content(request, **kwargs):
    prefix = "artist:"
    resource_name = urllib.unquote_plus(kwargs['artist'])
    resource_id = prefix + resource_name
    content_key = urllib.unquote_plus(kwargs['content_key'])
    page = request.GET.get('page')

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'page': page,
        'use_generic_key': True,
        'description': kwargs.get('description'),
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_name),
    }

    if content_key == "song_playlist":
        service_map[content_key] = services.Playlist(resource_name)
    elif content_key == "similar_artists": 
        service_map[content_key] = services.SimilarArtists(resource_name)
    elif content_key == "songs":
        service_map[content_key] = services.ArtistSongs(resource_name)

    content = utils.generate_content(resource_id, service_map, page=page)
    if content_key in content:
        content['content'] = content.pop(content_key)
    context.update(content)

    return render(request, "artist-content.html", context)




def song_summary(request, **kwargs):
    prefix = "song:"
    artist = urllib.unquote_plus(kwargs['artist'])
    resource_name = urllib.unquote_plus(kwargs['song'])
    resource_id = prefix + resource_name

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'artist_name': artist,
        'use_generic_key': False,
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_name),
        'similar_artists': services.SimilarArtists(resource_name),
        'playlist': services.Playlist(resource_name, artist_id=artist),
    }

    content = utils.generate_content(resource_id, service_map)
    context.update(content)

    return render(request, "song-summary.html", context)




def song_content(request, **kwargs):
    prefix = "song:"
    artist = urllib.unquote_plus(kwargs['artist'])
    resource_name = urllib.unquote_plus(kwargs['song'])
    resource_id = prefix + resource_name
    content_key = urllib.unquote_plus(kwargs['content_key'])
    page = request.GET.get('page')

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'artist_name': artist,
        'page': page,
        'use_generic_key': True,
        'description': kwargs.get('description'),
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_name),
    }

    if content_key == "song_playlist":
        service_map[content_key] = services.Playlist(resource_name, artist_id=artist)
    elif content_key == "similar_artists": 
        service_map[content_key] = services.SimilarArtists(artist)

    content = utils.generate_content(resource_id, service_map, page=page)
    if content_key in content:
        content['content'] = content.pop(content_key)
    context.update(content)

    return render(request, "song-content.html", context)




"""
-------------------------------------
Functions for handling ASYNC requests
-------------------------------------
"""


def retrieve_content(request, **kwargs):
    resource_id = utils.unescape_html(request.GET.get('resource_id'))
    content_key = request.GET.get('content_key')
    page = request.GET.get('page')
    context = {}

    intermediate_data = cache.hget(resource_id, content_key)

    if intermediate_data:
        content = ast.literal_eval(intermediate_data)
        context['status'] = 'success'

        try:
            context[content_key] = utils.page_resource(page, content)
        except TypeError:
            context[content_key] = content

    else:
        context['status'] = 'pending'

    return HttpResponse(json.dumps(context), content_type="application/json")




# HTTP 500
def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


def clear_resource(request):
    resource = utils.unescape_html(request.GET.get('resource'))
    hit = cache.delete(resource)

    pre = "REMOVED," if hit else "NOT FOUND,"
    banner = '\'' * len(pre)

    print
    print banner
    print "%s %s" %(pre, resource)
    print banner
    print

    return HttpResponse(json.dumps({}), content_type="application/json")


def debug_template(request):

    return HttpResponse(json.dumps({}), content_type="application/json")
