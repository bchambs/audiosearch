from __future__ import absolute_import
import ast
# from functools import chain
import functools

from audiosearch import Cache
from audiosearch.conf import NROWS_DEFAULT
from audiosearch.core.processors import (
    StandardTemplateMapping,
    process_available, 
    process_failed, 
    # process_pending, 
    process_missing,
)


def dispatch(resource, status, page=None):
    """Resource processing router.  Fetch cached data if key is in cache, assign 
    an appropriate error message if retrieval failed, or defer retrieval if key
    was not found.

    Return a dict representing `resource`'s template context.
    """

    # Fetch necessary values then map processed data to template-ready dict
    if status == 'available':
        if resource.echo_type is list:
            start, end = _calculate_range(page)
            raw_data, size, converter = _fetch_list(resource.key, start, end)
            content_map = process_available(raw_data, converter, size, page,
                start, end)

        elif resource.echo_type is dict:
            raw_data, converter = _fetch_hash(resource.key)
            content_map = process_available(raw_data, converter, page)
        
        else:
            # Unexpected type  
            pass

    # Add error message to be displayed for resource's content body in template
    elif status == 'failed':
        content_map = process_failed()

    # TODO: implement
    # elif status == 'pending':
    #     pass

    # Enqueue retrieval task then add ajax opts to content map
    else:
        resource.retrieve()
        content_map = process_missing(resource.async_rep, page)

    # Combine generated content map with common context key:value pairs
    standard = StandardTemplateMapping(resource)
    processed = functools.chain(content_map.iteritems(), standard.iteritems())

    return dict(processed)


def _calculate_range(page):
    """Simple paginate function to create appropriate list indices."""

    if page:
        start = int(page) * NROWS_DEFAULT
        end = start + NROWS_DEFAULT
    else:
        start = 0
        end = NROWS_DEFAULT - 1

    return start, end


def _fetch_list(key, start, end):
    """The operations and conversion function executed for all echo resources 
    stored as a redis list.
    """
    raw_data = Cache.get_list(key, start, end)
    size = Cache.get_list_size(key)
    converter = lambda data_list: [ast.literal_eval(i) for i in data_list]

    return raw_data, size, converter


def _fetch_hash(key):
    """The operations and conversion function executed for all echo resources 
    stored as a redis hash.
    """
    raw_data = Cache.get_hash(key)
    converter = lambda data_dict: ast.literal_eval(data_dict)

    return raw_data, converter
