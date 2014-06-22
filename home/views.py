import tasks
import util
import json

from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

from audiosearch.redis import client as RC
from home.models import ENCall, ARTIST_BUCKET
from util import debug, debug_title

"""
Convention: 
    dict['status'] for request state:
        ready,
        pending,
        failed
    dict['message'] for explanation
"""

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

    # MISS: create request package, defer call, return pending context
    debug_title ("MISS: %s" % request_id)

    package = ENCall('artist', 'profile')
    package.build(request_id, bucket=ARTIST_BUCKET)
    tasks.call_API.delay(package)

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
def async_retrieve_general(request):
    request_id = request.GET['q']

    data = {}
    data_str = RC.get(request_id)
    data = json.loads(data_str) if data_str else {'status': 'pending'}

    return HttpResponse(json.dumps(data), content_type="application/json")
