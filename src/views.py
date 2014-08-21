import ast
import json
import urllib

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

import audiosearch.config as cfg
from src import services, utils, tasks
from audiosearch.redis import client as cache




def index(request, **kwargs):
    context = Context({})

    return render(request, 'index.html', context)



# Content displayed is determined by 'type' query param from GET dict.
def search(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)

    q = normal_GET.get('q')

    if not q:
        context = {
            'search_artists': {
                'empty': cfg.EMPTY_MSG,
            },
            'search_songs': {
                'empty': cfg.EMPTY_MSG,
            },
        }
        return render(request, "search.html", context)

    prefix = "search:"
    resource_name = urllib.unquote_plus(q)
    resource_id = prefix + resource_name
    page = normal_GET.get('page')
    page_type = normal_GET.get('type')

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'page': page,
        'page_type': page_type,
        'data_is_paged': True if page_type else False,
        'use_generic_key': True if page_type else False,
        'display_by_artist': True,

        'debug': normal_kwargs.get('debug'),
    })

    service_map = {}

    if page_type == "artists":
        service_map['search_artists'] = services.SearchArtists(resource_name)
        context['content_description'] = "Artist results"
        context['q_params'] = {
            'q': resource_name,
            'type': page_type,
        }
    
    elif page_type == "songs":
        service_map['search_songs'] = services.SearchSongs(resource_name)
        context['content_description'] = "Song results"
        context['q_params'] = {
            'q': resource_name,
            'type': page_type,
        }

    else:
        service_map['search_artists'] = services.SearchArtists(resource_name)
        service_map['search_songs'] = services.SearchSongs(resource_name)

    content = utils.generate_content(resource_id, service_map, page=page)
    if page_type == "artists" and 'search_artists' in content:
        content['content'] = content.pop('search_artists')

    elif page_type == "songs" and 'search_songs' in content:
        content['content'] = content.pop('search_songs')

    context.update(content)

    return render(request, "search.html", context)



# Currently only displays the top 100 artists according to Echo Nest.
# I have tried to include multiple 'top content' items, but the results
# are lackluster.  Commented code is for the top 100 songs.
def music_home(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)

    prefix = "top:"
    resource_name = "music"
    resource_id = prefix + resource_name
    page = normal_GET.get('page')
    # page_type = normal_GET.get('type')
    # content_key = normal_kwargs.get('content_key')
    content_key = 'top_artists'

    context = Context({
        'resource_id': resource_id,
        'resource_name': "Trending Music",
        'content_description': "Popular Artists",
        'page': page,
        # 'page_type': page_type,
        # 'data_is_paged': True if page_type else False,
        'data_is_paged': True,
        'use_generic_key': True,

        'debug': normal_kwargs.get('debug'),
    })

    service_map = {
        'top_artists': services.TopArtists(),
    }

    content = utils.generate_content(resource_id, service_map, page=page)
    context.update(content)

    # service_map = {}
    
    # if page_type == "songs":
    #     service_map['top_songs'] = services.TopSongs()
    #     context['content_description'] = "Popular Songs"
    #     context['q_params'] = {
    #         'type': page_type,
    #     }

    # else:
    #     service_map['top_artists'] = services.TopArtists()
    #     context['content_description'] = "Popular Artists"
    #     context['q_params'] = {
    #         'type': page_type,
    #     }

    # content = utils.generate_content(resource_id, service_map, page=page, item_count=result_count)

    # if 'top_artists' in content:
    #     content['content'] = content.pop('top_artists')

    # elif 'top_songs' in content:
    #     print content['top_songs']['data'][0].keys()
    #     content['content'] = content.pop('top_songs')

    # context.update(content)

    return render(request, 'music_home.html', context)



# Display an artist's profile and top 15 songs.
# url: /music/artist
def artist_home(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)
    resource_name = urllib.unquote_plus(normal_kwargs.get('artist'))
    
    if not resource_name:
        return redirect(top_artists)

    prefix = "artist:"
    resource_id = prefix + resource_name
    track_count = 15

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'content_description': "Popular Tracks",
        'home_page': True,
        'data_is_paged': False,
        'use_generic_key': False,
        'item_count': track_count,

        'debug': normal_kwargs.get('debug'),
    })

    service_map = {
        'profile': services.ArtistProfile(resource_name),
        'songs': services.ArtistSongs(resource_name),
    }

    content = utils.generate_content(resource_id, service_map, item_count=track_count)
    context.update(content)

    return render(request, "artist-home.html", context)



# Display content table for an artist.
# Content displayed is determined by var passed from urls.py.
# url: /music/artist/+(content_key)
def artist_content(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)
    resource_name = urllib.unquote_plus(normal_kwargs.get('artist'))

    prefix = "artist:"
    resource_id = prefix + resource_name
    content_key = normal_kwargs.get('content_key')
    page = normal_GET.get('page')

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'page': page,
        'data_is_paged': True,
        'use_generic_key': True,
        'content_description': kwargs.get('description'),

        'debug': normal_kwargs.get('debug'),
    })

    service_map = {}

    if content_key == "song_playlist":
        service_map[content_key] = services.Playlist(resource_name)
        context['display_by_artist'] = True
    
    elif content_key == "similar_artists": 
        service_map[content_key] = services.SimilarArtists(resource_name)
    
    elif content_key == "songs":
        service_map[content_key] = services.ArtistSongs(resource_name)

    content = utils.generate_content(resource_id, service_map, page=page)
    if content_key in content:
        content['content'] = content.pop(content_key)
    context.update(content)

    return render(request, "artist-content.html", context)



# Display a songs's profile and top 15 similar songs.
# url: /music/artist/_/song
# The underscore will be replaced with album data if Echo Nest implements
# this information in the future. 
def song_home(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)
    resource_name = urllib.unquote_plus(normal_kwargs.get('song'))
    artist = urllib.unquote_plus(normal_kwargs.get('artist'))

    prefix = "song:"
    resource_id = prefix + artist + ":" + resource_name
    track_count = 15

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'artist_name': artist,
        'home_page': True,
        'data_is_paged': False,
        'use_generic_key': False,
        'display_by_artist': True,
        'item_count': track_count,

        'debug': normal_kwargs.get('debug'),
    })

    service_map = {
        'profile': services.SongProfile(resource_name, artist),
        'song_playlist': services.Playlist(resource_name, artist_id=artist),
    }

    content = utils.generate_content(resource_id, service_map, item_count=track_count)
    context.update(content)

    return render(request, "song-home.html", context)



# Display content table for a song.
# Content displayed is determined by var passed from urls.py.
# url: /music/artist/_/song/+(content_key)
def song_content(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)
    resource_name = urllib.unquote_plus(normal_kwargs.get('song'))
    artist = urllib.unquote_plus(normal_kwargs.get('artist'))

    prefix = "song:"
    resource_id = prefix + artist + ":" + resource_name
    content_key = normal_kwargs.get('content_key')
    page = normal_GET.get('page')

    context = Context({
        'resource_id': resource_id,
        'resource_name': resource_name,
        'artist_name': artist,
        'page': page,
        'data_is_paged': True,
        'use_generic_key': True,
        'content_description': normal_kwargs.get('description'),

        'debug': normal_kwargs.get('debug'),
    })

    service_map = {}

    if content_key == "song_playlist":
        service_map[content_key] = services.Playlist(resource_name, artist_id=artist)
        context['display_by_artist'] = True
        
    elif content_key == "similar_artists": 
        service_map[content_key] = services.SimilarArtists(artist)

    content = utils.generate_content(resource_id, service_map, page=page)
    if content_key in content:
        content['content'] = content.pop(content_key)
    context.update(content)

    return render(request, "song-content.html", context)



# About page.
# url: /about/
def about(request, **kwargs):
    context = Context({})

    return render(request, "about.html", context)




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

# Ajax target for retrieving pending content items.
# url: /ajax/retrieval/
def retrieve_content(request, **kwargs):
    normal_GET = utils.normalize(request.GET)
    normal_kwargs = utils.normalize(kwargs)

    resource_id = normal_GET.get('resource_id')
    resource_id = utils.unescape_html(resource_id)
    content_key = normal_GET.get('content_key')
    page = normal_GET.get('page')
    item_count = normal_GET.get('item_count')

    json_context = {}

    cache_data = cache.hget(resource_id, content_key)

    if cache_data:
        content = ast.literal_eval(cache_data)
        json_context['status'] = content.get('status')

        if json_context['status'] == "complete":
            json_context['data'] = utils.page_resource(page, content.get('data'), item_count)

    return HttpResponse(json.dumps(json_context), content_type="application/json")



# Remove resource_id from cache.
# For debugging only.
def clear_resource(request):
    normal_GET = utils.normalize(request.GET)

    resource_id = normal_GET.get('resource_id')
    print resource_id
    resource_id = utils.unescape_html(resource_id)
    print resource_id

    hit = cache.delete(resource_id)

    pre = "REMOVED," if hit else "NOT FOUND,"
    banner = '\'' * len(pre)

    print
    print banner
    print "%s %s" %(pre, resource_id)
    print banner
    print

    return HttpResponse(json.dumps({}), content_type="application/json")



