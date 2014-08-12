import sys
import ast

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import audiosearch.config as cfg
import tasks
from audiosearch.redis import client as cache




def generate_content(resource_id, service_map, **kwargs):
    page = kwargs.get('page')
    item_count = kwargs.get('item_count')
    result = {
        'pending_content': [],
    }

    if resource_id:
        resource_id = resource_id.lower()
        ####
        pipe = cache.pipeline()

        pipe.hget(resource_id, 'status')
        pipe.hget(resource_id, 'pending')
        status, pending = pipe.execute()

        # resource has been requested
        if status:
            # all content is ready
            if status == "complete":

            else:
            LOOP THROUGH SERVICE_MAP HERE:
                # if content_key is in pending, add to pending dict
                if key in pending:

                # queue content
                else:

        # resource has not been requested yet, queue entire service_map
        else:







        old
        # resource has been requested
        if status:
            # all content is ready
            if status == "complete":

            # some content is pending
            elif pending:
                # if content_key is in pending, add to pending dict
                if key in pending:

                # queue content
                else:

            # else queue entire service_map
            else

        # resource has not been requested yet, queue entire service_map
        else:


        add status / pending message to task

        ####
        cache_data = cache.hgetall(resource_id)

        for key, service in service_map.items():
            if key in cache_data:
                cache.expire(resource_id, service.ttl) # refresh TTL

                content = ast.literal_eval(cache_data[key])
                
                try:
                    result[key] = page_resource(page, content, item_count)
                except TypeError:
                    result[key] = content
            else:
                tasks.call.delay(resource_id, service, key)
                result['pending_content'].append(key)


    return result





def page_resource(page, resource, item_count=None):
    count = item_count or cfg.ITEMS_PER_PAGE
    paginator = Paginator(resource, count)

    try:
        paged = paginator.page(page)
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # need to do this because we can't serialize paginator objects in async call
    result = {
        'data': paged.object_list,
        'next': paged.next_page_number() if paged.has_next() else None,
        'previous': paged.previous_page_number() if paged.has_previous() else None,
        'current': paged.number,
        'total': paged.paginator.num_pages,
        'offset': paged.start_index(),
    }

    return result




def unescape_html(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")

    return s




def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    if len(percent) > 0:
        return percent[0] + " %"
    else:
        return ''



def convert_seconds(t):
    time = str(t)
    minutes = time.split('.')[0]

    if len(minutes) > 1:
        m = int(minutes) / 60
        s = round(t - (m * 60))
        seconds = str(s).split('.')[0]

        if len(seconds) < 2:
            seconds = seconds + "0"

        result['duration'] = "(%s:%s)" %(m, seconds)
    else:
        result['duration'] = "(:%s)" %(minutes[0])
