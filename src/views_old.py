from __future__ import absolute_import

import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch.redis_client import query
from src.content import ARTIST, ARTISTS, SEARCH, SONG, SONGS, TOP, TRENDING
import src.content as content
import src.debug as debug
import src.tasks as tasks




def index(request, **kwargs):
    context = Context({})

    return render(request, 'index.html', context)



# Content displayed is determined by 'type' query param from GET dict.
def search(request, **kwargs):
    # normal_GET = normalize(request.GET)
    # normal_kwargs = normalize(kwargs)

    q = normal_GET.get('q')

    # Return 'no results' search page.
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

        
    })

    service_map = {}

    # Use q_params to change default urls in content templates.
    if page_type == "artists":
        service_map['search_artists'] = SearchArtists(resource_name)
        context['content_description'] = "Artist results"
        context['q_params'] = {
            'q': resource_name,
            'type': page_type,
        }
    
    elif page_type == "songs":
        service_map['search_songs'] = SearchSongs(resource_name)
        context['content_description'] = "Song results"
        context['q_params'] = {
            'q': resource_name,
            'type': page_type,
        }

    else:
        service_map['search_artists'] = SearchArtists(resource_name)
        service_map['search_songs'] = SearchSongs(resource_name)

    content = generate_content(resource_id, service_map, trending_track=False, page=page)
    if page_type == "artists" and 'search_artists' in content:
        content['content'] = content.pop('search_artists')

    elif page_type == "songs" and 'search_songs' in content:
        content['content'] = content.pop('search_songs')

    context.update(content)

    return render(request, "search.html", context)



# Trending items. In dev.
def trending(request, **kwargs):
    # normal_GET = normalize(request.GET)
    # normal_kwargs = normalize(kwargs)

    prefix = "trending:"
    resource_name = "content"
    resource_id = prefix + resource_name

    context = Context({
        'resource_id': resource_id,
        'resource_name': "Trending Music",
        'content_description': "Popular Artists",
        'data_is_paged': True,
        'use_generic_key': True,

        
    })

    context['content'] = cache.hgetall(resource_id)

    return render(request, 'trending.html', context)



# Currently only displays the top 100 artists according to Echo Nest.
def music_home(request, **kwargs):
    resources = [
        content.Top100(ARTISTS),
    ]
    page = kwargs.get('page')
    n_items = 15
    is_home_page = page < 2

    available, failed, new, pending = query(resources)

    if new:
        generate_resources(new)

    complete = create_template_content(available, page, n_items, 
        is_home_page) if available else []

    context = Context({
        'resource': "top::None::artists",
        'title': "Popular Artists",
        'page': page,
        'n_items': n_items,
        'complete': complete,
        'failed': failed,
        'pending': pending + new,
    })

    debug.query(complete, failed, new, pending)

    return render(request, 'music-home.html', context)



# Display an artist's profile and top 15 songs.
# url: /music/artist
def artist_home(request, **kwargs):
    artist = kwargs.get('artist')
    
    if not artist:
        return redirect(music_home)

    resources = [
        content.ArtistProfile(artist),
        content.ArtistSongs(artist),
    ]
    item_count = 15

    complete, failed, new, pending = query(resources, item_count=item_count)

    if new:
        generate_resources(new)

    context = Context({
        'rows': item_count,
        'complete': complete,
        'failed': failed,
        'pending': pending + new,
    })

    try:
        asdf = context['content']['artist_songs']
        data = asdf['data']
        print asdf.keys()
        print len(data)
    except KeyError:
        pass

    return render(request, 'artist-home.html', context)



# Display content table for an artist.
# Content displayed is determined by var passed from urls.py.
# url: /music/artist/+(content_key)
def artist_content(request, **kwargs):
    # normal_GET = normalize(request.GET)
    # normal_kwargs = normalize(kwargs)
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

        
    })

    service_map = {}

    if content_key == "song_playlist":
        service_map[content_key] = Playlist(resource_name)
        context['display_by_artist'] = True
    
    elif content_key == "similar_artists": 
        service_map[content_key] = SimilarArtists(resource_name)
    
    elif content_key == "songs":
        service_map[content_key] = ArtistSongs(resource_name)

    content = generate_content(resource_id, service_map, page=page)
    if content_key in content:
        content['content'] = content.pop(content_key)
    context.update(content)

    return render(request, "artist-content.html", context)



# Display a songs's profile and top 15 similar songs.
# url: /music/artist/_/song
# The underscore will be replaced with album data if Echo Nest implements
# this information in the future. 
def song_home(request, **kwargs):
    # normal_GET = normalize(request.GET)
    # normal_kwargs = normalize(kwargs)
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

        
    })

    service_map = {
        'profile': SongProfile(resource_name, artist),
        'song_playlist': Playlist(resource_name, artist_id=artist),
    }

    content = generate_content(resource_id, service_map, item_count=track_count)
    context.update(content)

    return render(request, "song-home.html", context)



# Display content table for a song.
# Content displayed is determined by var passed from urls.py.
# url: /music/artist/_/song/+(content_key)
def song_content(request, **kwargs):
    # normal_GET = normalize(request.GET)
    # normal_kwargs = normalize(kwargs)
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

        
    })

    service_map = {}

    if content_key == "song_playlist":
        service_map[content_key] = Playlist(resource_name, artist_id=artist)
        context['display_by_artist'] = True
        
    elif content_key == "similar_artists": 
        service_map[content_key] = SimilarArtists(artist)

    content = generate_content(resource_id, service_map, page=page)
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
    # resource_id = kwargs.get('resource_id')
    # content_key = kwargs.get('content_key')
    # page = kwargs.get('page')
    # item_count = kwargs.get('item_count')
    # json_context = {}

    # cache_data = cache.hget(resource_id, content_key)

    # if cache_data:
    #     content = ast.literal_eval(cache_data)
    #     json_context['status'] = content.get('status')

    #     if json_context['status'] == "complete":
    #         json_context['data'] = page_resource(page, content.get('data'), item_count)

    # return HttpResponse(json.dumps(json_context), content_type="application/json")
    return HttpResponse(json.dumps({}), content_type="application/json")


# Remove resource_id from cache.
# For debugging only.
def clear_resource(request, **kwargs):
    from audiosearch.redis_client import _cache
    resource = kwargs.get('resource')

    hit = _cache.delete(resource)
    pre = "REMOVED," if hit else "NOT FOUND,"
    banner = '\'' * 14
    print banner
    print "%s %s" %(pre, resource)
    print banner

    return HttpResponse(json.dumps({}), content_type="application/json")




def generate_resources(new):
    for resource in new:
        service = resource.build_service()
        tasks.call_echo_nest.delay(resource.key, service, resource.ttl)





def create_template_content(resource_map, page, n_items, is_home_page):
    complete = {}

    for resource, content in resource_map.items():
        template_content = {
            'div_id': resource.template_id,
            'title': resource.title,
            'display_page_nav': is_home_page,
        }
        paged_content = page_content(content, page, n_items)
        template_content.update(paged_content)
        complete[resource.template_id] = template_content

    return complete



# Create content dict for generate template tables. 
def page_content(content, page, n_items):
    paginator = Paginator(content, n_items)

    try:
        paged = paginator.page(page)
    except AttributeError:          # Do not page dicts or strs.
        return content
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # Need to create paged dict because we cannot seralize Django's paged class.
    paged_content = {
        'data': paged.object_list,
        'next': paged.next_page_number() if paged.has_next() else None,
        'previous': paged.previous_page_number() if paged.has_previous() else None,
        'current': paged.number,
        'total': paged.paginator.num_pages,
        'offset': paged.start_index(),
    }

    return paged_content
