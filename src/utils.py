import sys
import ast

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import audiosearch.config as cfg
import tasks
from audiosearch.redis import client as cache


def generate_content(resource_id, service_map, **kwargs):
    intermediate_data = cache.hgetall(resource_id)
    page = kwargs.get('page')
    result = {
        'pending_content': [],
    }

    if intermediate_data:

    else:
        for key, service in service_map.items():
            tasks.call.delay(resource_id, service)
            result['pending_content'].append(required)

    return result



def generate_content_old(resource, service_map, **kwargs):
    cache_data = cache.hgetall(resource)
    page = kwargs.get('page')
    result = {
        'pending_content': [],
    }

    print "generating for: %s" %(resource)

    for key, service in service_map.items():
        if key in cache_data:

            print "HIT: %s" %(key)

            content = ast.literal_eval(cache_data[key])
            
            try:
                result[key] = page_resource(page, content)
            except TypeError:
                result[key] = content
        else:
            tasks.call.delay(resource, service)
            result['pending_content'].append(key)

            print "MISS: %s" %(key)

    return result





def page_resource(page, resource):
    result = {}
    paginator = Paginator(resource, cfg.ITEMS_PER_PAGE)

    try:
        paged = paginator.page(page)
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # need to do this because we can't serialize paginator objects in async call
    result['data'] = paged.object_list
    result['next'] = paged.next_page_number() if paged.has_next() else None
    result['previous'] = paged.previous_page_number() if paged.has_previous() else None
    result['current'] = paged.number
    result['total'] = paged.paginator.num_pages
    result['offset'] = paged.start_index()

    return result


def unescape_html(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")

    return s
