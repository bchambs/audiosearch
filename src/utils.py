import sys
import ast

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import audiosearch.config as cfg
import tasks
from audiosearch.redis import client as cache




def generate_content(resource_id, service_map, **kwargs):
    if not resource_id: return {}

    new_content = []
    pending_content = []
    result = {}

    page = kwargs.get('page')
    item_count = kwargs.get('item_count')
    resource_id = resource_id.lower()

    cache_data = cache.hgetall(resource_id)
    pipe = cache.pipeline()

    if cache_data:
        for key, service in service_map.items():
            if key in cache_data:
                content = ast.literal_eval(cache_data[key])

                if content['status'] == "complete":
                    result[key] = page_resource(page, content['data'], item_count)

                elif content['status'] == "pending":
                    pending_content.append(key)

                elif content['status'] == "failed":
                    result[key] = {'error_message': content['error_message']}

            # new content request
            else:   
                new_content.append(key)
                pending_content.append(key)

    else:   
        new_content = service_map.keys()
        pending_content = new_content

    for item in new_content:
        content_struct = {
            'status': "pending",
        }

        tasks.acquire_resource.delay(resource_id, item, service_map[item])
        pipe.hset(resource_id, item, content_struct)

    pipe.expire(resource_id, cfg.REDIS_TTL)
    pipe.execute()

    result['pending_content'] = pending_content

    return result




def page_resource(page, resource, item_count=None):
    try:
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

    except TypeError:
        return resource




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
