from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch.cache.client import client
from audiosearch.resources import artist
from audiosearch.resources.base import build_template_map


def music_home(request, **kwargs):
    # resources = []

    # page = kwargs.get('page')
    # n_items = 15
    # nav = NAV_STYLE.more
    # resources = [
    #     resource.Top100(ARTISTS),
    # ]

    # available, failed, new, pending = _get_cache_status(resources)

    # # if new:
    # #     _generate_resource_data(new)

    # if available:
    #     complete = build_content_from_data(available, nav, page, n_items)
    # else:
    #     complete = []

    # context = Context({
    #     'resource': "top::none::artists",
    #     'page': page,
    #     'n_items': n_items,
    #     'complete': complete,
    #     'failed': failed,
    #     'pending': pending + new,
    # })
    context = Context({})

    return render(request, 'music-home.html', context)


def artist_home(request, **kwargs):
    artist_name = kwargs.get('artist')
    page = kwargs.get('page')
    n_items = 15

    if not artist_name:
        return redirect(music_home)

    content = [
        artist.ArtistProfile(artist_name),
    ]

    available, failed, pending = client.fetch_all(content)

    print
    print len(available)
    print len(failed)
    print len(pending)
    print

    context = Context({
        'resource': "top::none::artists",
        'page': page,
        'n_items': n_items,
        'complete': build_template_map(available),
        'failed': build_template_map(failed),
        'pending': pending,
    })

    return render(request, 'artist-home.html', context)


# def _generate_resource_data(new_resources):
#     for resource in new_resources:
#         service = resource.build_service()
#         call_echo_nest.delay(resource.key, resource.ttl, service)


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

