import tasks
import util
import ast
import json

from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

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


def search(request):
    """
    /search/
    """

    search_name = request.GET['q'].lower()
    context = Context({})

    RC.delete(search_name)

    if search_name:
        result = RC.hgetall(search_name)

        if 'artists' in result:
            context['artists'] = ast.literal_eval(result['artists'])[:15]
        else:
            tasks.call_service.delay(ArtistSearch(search_name))

        if 'songs' in result:
            context['songs'] = ast.literal_eval(result['songs'])[:15]
        else:
            tasks.call_service.delay(SongSearch(search_name))
    else:
        context['empty'] = True

    return render(request, 'search.html', context)


def artist_info(request):
    """
    /artist/
    """
    artist_id = request.GET['q']

    # TODO: remove
    # RC.delete(artist_id)


    context = Context({})
    artist = RC.hgetall(artist_id)

    if 'profile' in artist:
        context['profile'] = ast.literal_eval(artist['profile'])
    else:
        tasks.call_service.delay(ArtistProfile(artist_id))

    if 'songs' in artist:
        context['songs'] = ast.literal_eval(artist['songs'])
        context['songs'] = context['songs'][:15]
    else:
        tasks.call_service.delay(Playlist(artist_id))

    if 'similar' in artist:
        context['similar'] = ast.literal_eval(artist['similar'])
        context['similar'] = context['similar'][:15]
    else:
        tasks.call_service.delay(SimilarArtists(artist_id))

    return render(request, 'artist.html', context)

    # packages = []

    # if 'profile' in artist:
    #     context['profile'] = ast.literal_eval(artist['profile'])
    # else:
    #     packages.append(ArtistProfile(artist_id))

    # if 'songs' in artist:
    #     context['songs'] = ast.literal_eval(artist['songs'])
    # else:
    #     packages.append(Playlist(artist_id))

    # if 'similar' in artist:
    #     context['similar'] = ast.literal_eval(artist['similar'])
    # else:
    #     packages.append(SimilarArtists(artist_id))

    # # MISS: defer call
    # if packages:
    #     tasks.call_service.delay(packages)

    # return render(request, 'artist.html', context)


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


