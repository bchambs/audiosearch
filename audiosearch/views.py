from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch.cache.client import client
from audiosearch.handlers import miss
from audiosearch.resources import (discography, playlist, profile, search, 
    similar, top)
from audiosearch.resources.template import (build_template_map, NAV_MORE, 
    NAV_PAGES)

def reset(view_func):
    def _decorator(request, *args, **kwargs):
        client.flushall()
        response = view_func(request, *args, **kwargs)
        return response
    return wraps(view_func)(_decorator)


def artist_home(request, GET, opt):
    try:
        artist = opt.pop('artist')
    except KeyError:
        return redirect(music_home)

    page = GET.get('page')
    n_items = 15

    resources = [
    ]

    # handler = miss.get_echo_data
    # available, failed, pending = client.fetch_all(resources, handler)

    # content = build_template_map(available, failed, page, n_items, NAV_MORE)

    # print
    # print len(available)
    # print len(failed)
    # print len(pending)
    # print

    # context = Context({
    #     'resource': "top::none::artists",
    #     'page': page,
    #     'n_items': n_items,
    #     'content': content, 
    #     'pending': pending,
    # })

    context = Context({})
    return render(request, 'artist-home.html', context)


def music_home(request, GET, opt):
    context = Context({})
    return render(request, 'music-home.html', context)
    

# def clear_resource(request, **kwargs):
#     """Remove resource.key from cache."""

#     from audiosearch.redis_client import _cache

#     try:
#         resource = kwargs.pop('resource')
#     except KeyError:
#         return HttpResponse(json.dumps({}), content_type="application/json")

#     hit = _cache.delete(resource)
#     pre = "REMOVED," if hit else "NOT FOUND,"
#     banner = '\'' * 14
#     print banner
#     print "%s %s" %(pre, resource)
#     print banner

#     return HttpResponse(json.dumps({}), content_type="application/json")



