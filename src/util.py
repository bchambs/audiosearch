# from __future__ import absolute_import
from random import choice, sample
import logging
import sys
import ast

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import audiosearch.config as cfg


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


def print_cache(c, indent=0):
   for key, value in c.iteritems():
      print '   ' * indent + str(key)
      if isinstance(value, dict):
         print_cache(value, indent+1)
      else:
         # print '    ' * (indent+1) + str(value)
         pass
