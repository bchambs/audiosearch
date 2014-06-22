import tasks
import util
import json

from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

from audiosearch.redis import client as RC
from util import debug, debug_title
from home.models import ENCall, ARTIST_BUCKET

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
    # HIT: get json, convert to dict, and return complete page
    if RC.exists(request_id):
        artist_str = RC.get(request_id)
        artist_dict = json.loads(artist_str)

        context.update(artist_dict)
        context['served'] = True

        debug_title('hit: %s' % request_id)

        return render(request, 'artist.html', context)

    # MISS: create request package, defer call, return pending context
    package = ENCall('artist', 'profile')
    package.build(request_id, bucket=ARTIST_BUCKET)
    tasks.call_API.delay(package)

    context['served'] = False
    debug_title('miss: %s' % request_id)

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

# async requests for general artist / song data
def async_retrieve_general(request):
    request_id = request.GET['q']
    data = {}
   
    if RC.exists(request_id):
        data_str = RC.get(request_id)
        data = json.loads(data_str)
        data['status'] = 'ready'
    
    else:
        data['status'] = 'retry'

    return HttpResponse(json.dumps(data), content_type="application/json")
