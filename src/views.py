from __future__ import absolute_import
import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch.constants import AVAIL, FAIL, NEW, PEND
from audiosearch.redis_client import fetch
from src.content import ARTIST, ARTISTS, SEARCH, SONG, SONGS, TOP, TRENDING
import src.content as content
import src.debug as debug
import src.tasks as tasks


def music_home(request, **kwargs):
    page = kwargs.get('page')
    n_items = 15            # Rows displayed.
    summary_page = True     # Use content summary template.
    resources = [
        content.Top100(ARTISTS),
    ]

    available, failed, new, pending = check_cache(resources)


    if new:
        generate_resource_data(new)

    complete = map_content_to_template(available) if available else []

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


def check_cache(resources):
    """Build status list by resource availability."""

    # Resource status map. 
    s_map = {
        # Contains list of (resource, data) tuples.
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




def generate_resource_data(new_resources):
    for resource in new_resources:
        service = resource.build_service()
        tasks.call_echo_nest.delay(resource.key, service, resource.ttl)


def map_content_to_template(available_resources):
    for resource in available_resources:
        









def create_template_content(resource_map, page, n_items, is_home_page):
    complete = {}

    for resource, content in resource_map.items():
        template_content = {
            'div_id': resource.template_id,
            'title': resource.title,
            'display_page_nav': is_home_page,
        }
        paged_content = page_content(content, page, n_items)
        template_content.update(paged_content)
        complete[resource.template_id] = template_content

    return complete



def page_content(content, page, n_items):
    """Create content dict for generate template tables."""

    n_items = n_items or N_CONTENT_ROWS
    paginator = Paginator(content, n_items)

    try:
        paged = paginator.page(page)
    except AttributeError:          # Do not page dicts or strs.
        return content
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # Need to create paged dict because we cannot seralize Django's paged class.
    paged_content = {
        'data': paged.object_list,
        'next': paged.next_page_number() if paged.has_next() else None,
        'previous': paged.previous_page_number() if paged.has_previous() else None,
        'current': paged.number,
        'total': paged.paginator.num_pages,
        'offset': paged.start_index(),
    }

    return paged_content









    


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











    # # List of (resource, cache value) tuple for all available resources.
    # available = []

    # # List of unavailable resources grouped by status.
    # failed = []    
    # new = []
    # pending = []  

    # for resource in resources:
    #     status, value = query(resource.key, resource.ttl)

    #     if status == CACHE_CODE.available:
    #         available.append(resource, value)
    #     elif status == CACHE_CODE.failed:
    #         failed.append(resource)
    #     elif status == CACHE_CODE.pending:
    #         pending.append(resource)
    #     elif status == CACHE_CODE.new:
    #         new.append(resource)

    # return available, failed, new, pending
