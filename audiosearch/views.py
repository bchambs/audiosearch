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

    # try:
    #     raw_data = Cache.get(top.key, top.dispatch())
    # except FailedKeyError:
    #     process_failed(top)

    # status = Cache.get_status(top.key)
    # top_content = handlers.dispatch(top, status)
    # context[top.resource_id] = top_content

    return render(request, 'music-home.html', context)



def ajax_retrieve_content(request, GET, **params):
    context = dict(status='failed')
    return HttpResponse(json.dumps(context), content_type="application/json")
