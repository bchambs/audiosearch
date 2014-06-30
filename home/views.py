import tasks
import util
import json

from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

from audiosearch.redis import client as RC
from home.calls import ArtistProfile, Playlist, SimilarArtists
from util import debug, debug_title


"""
---------------------------
Functions for serving pages
---------------------------
"""

# /artist/
def artist_info(request):
    request_id = request.GET['q']
    context = Context({})

    # cache check
    artist_str = RC.get(request_id)

    # HIT: get json_str, convert to dict, return template
    if artist_str:
        debug_title ("HIT: %s" % request_id)

        artist_dict = json.loads(artist_str)
        context.update(artist_dict)

        return render(request, 'artist.html', context)

    # MISS: create request packages, defer call, return pending context
    debug_title ("MISS: %s" % request_id)

    packages = []

    profile = ArtistProfile(request_id)
    packages.append(profile)
    playlist = Playlist(request_id)
    packages.append(playlist)
    similar = SimilarArtists(request_id)
    packages.append(similar)

    tasks.call_service.delay(request_id, packages)

    context['status'] = 'pending'

    return render(request, 'artist.html', context)


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
    request_id = request.GET['q']

    data = {}
    data_str = RC.get(request_id)
    data = json.loads(data_str) if data_str else {'status': 'pending'}

    return HttpResponse(json.dumps(data), content_type="application/json")
