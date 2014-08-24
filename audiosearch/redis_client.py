from __future__ import absolute_import

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import redis

from audiosearch.constants import EMPTY, FAILED, PENDING


_HOST = 'localhost'
_PORT = 6379
_DATABASE = 0
_cache = redis.StrictRedis(host=_HOST, port=_PORT, db=_DATABASE)
_cache.client_setname("django_redis_client")


def query(resources, **kwargs):
    global _cache

    complete = {}
    failed = []
    new = []
    pending = []

    page = kwargs.get('page')
    item_count = kwargs.get('item_count')

    for resource in resources:
        if resource.TTL:
            _cache.expire(resource.TTL)

        key_type = _cache.type(resource.key)

        if key_type == "list":
            value = _cache.lrange(resource.key, 0,-1)
            complete[resource.content_id] = page_data(value, page, item_count)

        elif key_type == "string":
            value = _cache.get(resource.key)

            if value == PENDING:
                pending.append(resource)
            elif value == FAILED:
                failed.append(resource)
            else:
                complete[resource.content_id] = resource

        elif key_type == "hash":
            complete[resource.content_id] = _cache.hgetall(resource.key)

        # Resource not in cache.
        else:
            new.append(resource)    

    return complete, failed, new, pending



def store(key, value, ttl):
    global _cache

    if type(value) is list:
        _cache.rpush(key, *value)
    elif type(value) is str:
        _cache.set(str)
    elif type(value) is dict:
        _cache.hmset(key, value)

    if ttl:
        _cache.expire(key, ttl)



def page_data(value, page, item_count):
    count = item_count or constants.ITEMS_PER_PAGE
    paginator = Paginator(value, count)

    try:
        paged = paginator.page(page)
    except PageNotAnInteger:
        paged = paginator.page(1)
    except EmptyPage:
        paged = paginator.page(paginator.num_pages)

    # Need to create paged dict because we cannot seralize Django's paged class.
    result = {
        'data': paged.object_list,
        'next': paged.next_page_number() if paged.has_next() else None,
        'previous': paged.previous_page_number() if paged.has_previous() else None,
        'current': paged.number,
        'total': paged.paginator.num_pages,
        'offset': paged.start_index(),
    }

    return result

