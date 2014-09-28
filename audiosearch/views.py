from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import Context

from audiosearch import Cache
from audiosearch.core import echonest
from audiosearch.models import artist
from audiosearch.utils.decorators import reset_cache, stdout_gap


# @reset_cache('top')
@stdout_gap
def music_home(request, qstring, **kwargs):
    context = {}

    profile = artist.Profile('led zeppelin')

    if profile.key in Cache:
        # profile_data = Cache.get(profile.fetch)
        pass
    else:
        echonest.get(profile)

    return render(request, 'music-home.html', context)



def ajax_retrieve_content(request, GET, **kwargs):
    context = dict(status='failed')
    return HttpResponse(json.dumps(context), content_type="application/json")
