import tasks
import ast
import json

from django.shortcuts import render, redirect
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse

from audiosearch.settings import SEARCH_RESULT_DISPLAYED, ARTIST_SONGS_DISPLAYED, SIMILAR_ARTIST_DISPLAYED, REDIS_DEBUG, MORE_RESULTS
from audiosearch.redis import client as RC
from src.calls import ArtistProfile, Playlist, SimilarArtists, ArtistSearch, SongSearch


"""
---------------------------
Functions for serving pages
---------------------------
"""


def index(request):
    context = Context({})

    return render(request, 'index.html', context)


def search(request, qq=None, redirect_qq=None):
    """
    /search/
    """

    try:
        search_name = request.GET['q'].lower()
    except KeyError:
        search_name = 'asdf'

    context = Context({
        'q': search_name
    })

    if REDIS_DEBUG:
        RC.delete(search_name)

    if search_name:
        result = RC.hgetall(search_name)

        if 'artists' in result:
            artists = ast.literal_eval(result['artists'])
            context['artists_has_pages'] = True if len(artists) > SEARCH_RESULT_DISPLAYED else False
            context['artists'] = artists[:SEARCH_RESULT_DISPLAYED]
        else:
            tasks.call_service.delay(ArtistSearch(search_name))

        if 'songs' in result:
            context['songs'] = ast.literal_eval(result['songs'])[:15]
        else:
            tasks.call_service.delay(SongSearch(search_name))
    else:
        context['empty'] = True

    return render(request, 'search.html', context)


def more_artists_results(request):
    search_name = request.GET['q'].lower()
    page = request.GET.get('page')
    context = Context({
        'q': search_name
    })

    if REDIS_DEBUG:
        RC.delete(search_name)

    raw = RC.hget(search_name, 'artists')
    if raw:
        artists = ast.literal_eval(raw)
        paginator = Paginator(artists, MORE_RESULTS)

        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

        context['results'] = results
    else: 
        # return redirect('/search/', kwargs={'request':request, 'q':search_name})
        print 'q: %s' % search_name
        print 'redirecting'
        return redirect('/search/', q=search_name, redirect_q=search_name)

    return render(request, 'search-artists.html', context)


def artist_info(request):
    """
    /artist/
    """
    artist_id = request.GET['q']
    context = Context({
        'q': artist_id
    })

    if REDIS_DEBUG:
        RC.delete(artist_id)

    artist = RC.hgetall(artist_id)

    if 'profile' in artist:
        context['profile'] = ast.literal_eval(artist['profile'])
    else:
        tasks.call_service.delay(ArtistProfile(artist_id))

    if 'songs' in artist:
        context['songs'] = ast.literal_eval(artist['songs'])
        context['songs'] = context['songs'][:SEARCH_RESULT_DISPLAYED]
    else:
        tasks.call_service.delay(Playlist(artist_id))

    if 'similar' in artist:
        context['similar'] = ast.literal_eval(artist['similar'])
        context['similar'] = context['similar'][:SEARCH_RESULT_DISPLAYED]
    else:
        tasks.call_service.delay(SimilarArtists(artist_id))

    return render(request, 'artist.html', context)


def song_info (request):
    context = Context({})
    song_id = request.GET['q']

    return render(request, 'index.html', context)


# HTTP 500
def server_error(request):
    response = render(request, '500.html')
    response.status_code = 500
    return response


"""
-------------------------------------
Functions for handling ASYNC requests
-------------------------------------
"""

# check cache, if hit return json else return pending
def retrieve_resource(request):
    id_ = request.GET['q']
    resource = request.GET['resource']
    data = {}
    data_str = RC.hget(id_, resource)

    if data_str:
        data[resource] = ast.literal_eval(data_str)
        data['status'] = 'ready'

    else:
        data['status'] = 'pending'

    return HttpResponse(json.dumps(data), content_type="application/json")


