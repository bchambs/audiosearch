from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, RequestContext

from audiosearch import Cache
from audiosearch.conf.settings import NROWS_DEFAULT
from audiosearch.models import resource
from audiosearch.utils.decorators import reset_cache, stdout_gap


# @reset_cache('top')
@stdout_gap
def music_home(request, GET, **params):
    context = {}
    top = resource.TopArtists()

    print Cache
    
    if top in Cache:
        data = Cache.getlist(top.key, 0, 14)
        print data
    else:
        top.retrieve()

    return render(request, 'music-home.html', context)



def ajax_retrieve_content(request, GET, **params):
    context = dict(status='failed')
    return HttpResponse(json.dumps(context), content_type="application/json")
