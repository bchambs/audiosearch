from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse
from audiosearch.redis import client as RC
from util import debug, debug_title

import tasks
import util
import json

'''
---------------------------
Functions for serving pages
---------------------------
'''

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

        debug_title('hit')

        return render(request, 'artist.html', context)

    # MISS: create request package, defer call, return pending context
    debug_title('miss')
    tasks.call_API.delay(request_id, 'artist', 'profile')
    context['served'] = False

    return render(request, 'artist.html', context)


# HTTP 500
def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response


'''
-------------------------------------
Functions for handling ASYNC requests
-------------------------------------
'''
def async_retrieve(request):
    debug('in async_retrieve')

    request_id = request.GET['q']
    data = tasks.retrieve_json(query)
    
    debug('completed async_retrieve')
    print data[0]
    print data[1]

    return HttpResponse(data[1], content_type="application/json")

