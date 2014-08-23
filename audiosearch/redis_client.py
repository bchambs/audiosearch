from __future__ import absolute_import

import ast

import redis

from src.content import PENDING
from src.tasks import generate_resource


HOST = 'localhost'
PORT = 6379
DATABASE = 0
CONNECTIONS = 20

_cache = redis.StrictRedis(host=HOST, port=PORT, db=DATABASE)
_cache.client_setname("django_redis_client")


def query(resource_map, **kwargs):
    global _cache

    complete = {}
    failed = []
    pending = []

    page = kwargs.get('page')
    item_count = kwargs.get('item_count')

    for key in resource_map:
        key_type = _cache.type(key)

        print
        print key
        print key_type
        print resource_map[key]
        print


        if key_type == "list":
            resource = _cache.lrange(0,-1)
            complete[key] = page_resource(resource, page, item_count)

        elif key_type == "hash":
            resource = _cache.hgetall(resource_map[key])
            complete[key] = ast.literal_eval(resource)

        elif key_type == "string":
            resource = _cache.get(resource_map[key])

            if resource == PENDING:
                pending.append(key)
            elif resource == FAILED:
                failed.append(key)
            else:
                complete[key] = resource

        # Resource does not exist.  Queue service.
        else:
            generate_resource()

    return complete, pending



def store():
    global _cache
    


# Attempt to page a given resource (string, list, dict) by item_count or
# cfg.ITEMS_PER_PAGE
# If resource cannot be paged, return the resource.
def page_resource(resource, page, item_count):
    count = item_count or cfg.ITEMS_PER_PAGE
    paginator = Paginator(resource, count)

    try:
        paged = paginator.page(page)
    except TypeError:
        return resource
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # We must create our own paged context because we cannot seralize Django's paged class.
    result = {
        'data': paged.object_list,
        'next': paged.next_page_number() if paged.has_next() else None,
        'previous': paged.previous_page_number() if paged.has_previous() else None,
        'current': paged.number,
        'total': paged.paginator.num_pages,
        'offset': paged.start_index(),
    }

    return result

