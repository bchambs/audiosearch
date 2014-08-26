from __future__ import absolute_import
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch.constants import AVAIL, FAIL, NEW, PEND
from audiosearch.redis_client import fetch
from src.resource import ARTIST, ARTISTS, SEARCH, SONG, SONGS, TOP, TRENDING
from src.template import build_content_from_data, NAV_STYLE
import src.resource as resource
import src.tasks as tasks


def music_home(request, **kwargs):
    page = kwargs.get('page', 0)
    n_items = 15
    nav = NAV_STYLE.more
    resources = [
        resource.Top100(ARTISTS),
    ]

    available, failed, new, pending = _check_cache(resources)

    if new:
        _generate_resource_data(new)

    if available:
        complete = build_content_from_data(available, nav, page, n_items)
    else:
        complete = []

    context = Context({
        'resource': "top::none::artists",
        'title': "Popular Artists",
        'page': page,
        'n_items': n_items,
        'complete': complete,
        'failed': failed,
        'pending': pending + new,
    })

    return render(request, 'music-home.html', context)


def _check_cache(resources):
    """Build status list by resource availability."""

    # Resource status map. 
    s_map = {
        # Contains list of (resource, data) tuples.  (Cache hit).
        AVAIL: [],     

        # Lists of resource objects grouped by status.
        FAIL: [],           
        NEW: [],
        PEND: [],
    }

    for resource in resources:
        status, data = fetch(resource.key, resource.ttl)
        element = (resource, data) if data else resource
        s_map[status].append(element)
        print
        print "$$$$$$$$$$"
        print "KEY IS: %s" %resource.key
        print "RESOURCE IS: %s" %status
        # print s_map[status]
        print type(s_map[status])
        print "$$$$$$$$$$"
        print

    return s_map[AVAIL], s_map[FAIL], s_map[NEW], s_map[PEND]


def _generate_resource_data(new_resources):
    for resource in new_resources:
        service = resource.build_service()
        tasks.call_echo_nest.delay(resource.key, service, resource.ttl)


def clear_resource(request, **kwargs):
    """Remove resource.key from cache."""

    from audiosearch.redis_client import _cache

    try:
        resource = kwargs.pop('resource')
    except KeyError:
        return HttpResponse(json.dumps({}), content_type="application/json")

    hit = _cache.delete(resource)
    pre = "REMOVED," if hit else "NOT FOUND,"
    banner = '\'' * 14
    print banner
    print "%s %s" %(pre, resource)
    print banner

    return HttpResponse(json.dumps({}), content_type="application/json")

