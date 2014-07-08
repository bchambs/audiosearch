import tasks
import util
import ast
import json

from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

from audiosearch.redis import client as RC
from src.calls import ArtistProfile, Playlist, SimilarArtists
from util import debug, debug_title


"""
---------------------------
Functions for serving pages
---------------------------
"""


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
def async_artist(request):
    artist_id = request.GET['q']
    resource = request.GET['resource']
    data = {}
    data_str = RC.hget(artist_id, resource)

    if data_str:
        data[resource] = ast.literal_eval(data_str)
        data['status'] = 'ready'

    else:
        data['status'] = 'pending'

    return HttpResponse(json.dumps(data), content_type="application/json")

