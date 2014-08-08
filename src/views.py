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
    resource_id = urllib.unquote_plus(request.GET.get('q'))
    resource = prefix + resource_id
    page = request.GET.get('page')
    page_type = request.GET.get('type')   

    context = Context({
        'resource': resource,
        'resource_id': resource_id,
        'type': page_type,
        'page': page,
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'search_artists': services.SearchArtists(resource_id),
        'search_songs': services.SearchSongs(None, resource_id),
    }

    content = utils.generate_content(resource, service_map, page=page)
    context.update(content)

    # if page_type == "artists":
    #     context['type_content'] = mydict.pop(old_key)
    #     context['type_content'] = context['search_songs']
    # elif page_type == "songs":
    #     context['type_content'] = context['search_artists']
    # else
    #     context['type_content'] = None

    return render(request, "search.html", context)




# artist_service_map = {
#     'profile': lambda resource_name: services.ArtistProfile(resource_name),
#     'songs': lambda resource_name: services.ArtistSongs(resource_name),
#     'similar': lambda resource_name: services.SimilarArtists(resource_name),
#     'recommended': lambda resource_name: services.SongPlaylist(resource_name),
# }




def artist_summary(request, **kwargs):
    prefix = "artist:"
    resource_name = urllib.unquote_plus(kwargs['artist'])
    resource_id = prefix + resource_name

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'debug': kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_id),
        'songs': services.ArtistSongs(resource_id),
        'similar_artists': services.SimilarArtists(resource_id),
        'playlist': services.Playlist(resource_id),
    }

    # service_map = {
    #     'profile': artist_service_map['profile'],
    #     'songs': artist_service_map['songs'],
    #     'similar': artist_service_map['similar'],
    #     'recommended': artist_service_map['recommended'],
    # }

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

    # service_map = {
    #     'profile': artist_service_map['profile'](resource_name),
    #     content_key: artist_service_map[content_key](resource_name),
    # }

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
