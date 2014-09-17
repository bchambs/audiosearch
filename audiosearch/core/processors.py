"""Responsible for building resource dicts for template rendering."""

from __future__ import absolute_import
import ast

from audiosearch.conf import messages


def StandardTemplateMapping(resource):
    """Required key, value pairs regardless of status."""
    return {
        'div_id': resource.resource_id,
        'title': resource.description,
    }


def process_available(raw, convert, page, size=None, start=None, end=None):
    data = convert(raw)
    context = {
        'resource_data': data,
        'page': page,
        'has_next': end < size,
        'has_previous': start > size,
    }

    return context


def process_failed(): 
    return 1


# def process_pending(): pass


def process_missing(): 
    return 1


        
# class Available(object):
#     @staticmethod
#     def process(resource, data_string, size, start, end, page=None):
#         common = _build_common_map(resource)
#         converted = [ast.literal_eval(i) for i in data_string]
#         template_map = {
#             'resource_data': converted,
#             'page': page,
#             'has_next': end < size,
#             'has_previous': start > size,
#         }
#         combine = chain(template_map.iteritems(), common.iteritems())

#         return dict(combine)


# class Failed(object):
#     @staticmethod
#     def process(resource):
#         template_map = {
#             'error': messages.STORAGE_FAILURE,
#         }
#         common = _build_common_map(resource)
#         combine = chain(template_map.iteritems(), common.iteritems())

#         return dict(combine)


# class Pending(object):
#     @staticmethod
#     def process(resource, page=None):
#         template_map = {
#             'group': resource.group,
#             'category': resource.category,
#             'name': resource.name,
#             'qstring': {},  # Query string to be built with template tag
#         }

#         if page: 
#             template_map['qstring']['page'] = page

#         common = _build_common_map(resource)
#         combine = chain(template_map.iteritems(), common.iteritems())

#         return dict(combine)


# def _build_common_map(resource):
#     common = {
#         'div_id': resource.res_id,
#         'title': resource.description,
#     }
#     return common

