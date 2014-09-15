"""Responsible for building resource dicts for template rendering."""

from __future__ import absolute_import
import ast
from itertools import chain

        
# if resource.echo_type is list:
#     converted = [ast.literal_eval(i) for i in raw_data]
# else:
#     converted = ast.literal_eval(raw_data)
class Available(object):
    # TODO: see if this is equal to dict.update
    @staticmethod
    def process(resource, cache_response, page=None):
        raw_data, size = cache_response
        converted = ast.literal_eval(raw_data)
        has_next, has_prev = _paginate(page)
        common = _build_common_map(resource)

        template_map = {
            'resource_data': converted,
            'page': page,
            'has_next_page': has_next,
            'has_previous_page': has_prev,
        }

        return chain(template_map.iteritems(), common.iteritems())


class Failed(object):
    @staticmethod
    def process(resource, error_msg):
        template_map = {
            'error': error_msg,
        }
        common = _build_common_map(resource)
        template_map.update(common)

        return template_map



class Pending(object):
    @staticmethod
    def process(resource, page=None):
        template_map = {
            'group': resource.group,
            'category': resource.category,
            'div_id': resource.res_id,
            'name': resource.name,
            'qstring': {},  # Query string to be built with template tag
        }

        if page: 
            template_map['qstring']['page'] = page

        common = _build_common_map(resource)
        template_map.update(common)

        return template_map


def _build_common_map(resource):
    common = {
        'div_id': resource.res_id,
        'title': resource.title,
    }
    return common


def _paginate(page):
    if page:
        pass
    else:
        return False, False
