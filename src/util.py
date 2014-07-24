# from __future__ import absolute_import
from random import choice, sample
import logging
import sys
import ast

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import audiosearch.config as cfg


log = logging.getLogger("audiosearch")

def page_resource(page, resource):
    result = {}
    paginator = Paginator(resource, cfg.ITEMS_PER_PAGE)

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result


# paginator objects cannot be serialized, recreate everything we need
def page_resource_async(page, resource, rtype):
    result = {}
    paged = page_resource(page, resource) # TODO: rename something
    result[rtype] = paged.object_list
    result['has_next'] = True if paged.has_next() else False
    result['has_previous'] = True if paged.has_previous() else False
    result['current_page'] = paged.number
    result['total_pages'] = paged.paginator.num_pages
    result['offset'] = paged.start_index()

    try:
        result['previous_page_number'] = paged.previous_page_number()
    except EmptyPage:
        pass
    try:
        result['next_page_number'] = paged.next_page_number()
    except EmptyPage:
        pass

    return result


def inspect_response(response, service):
    """
    debug echo nest response 
    @response = request.get response
    """
    log.info("===%s" %(service))
    try:
        js = response.json()
    except ValueError, AttributeError:
        log.error("could not get json")
        return
        
    if js['response']['status']['code'] is not 0:
        log.warning("%s" % js['response']['status']['message'])
        return

    temp = js['response']
    del temp['status']
    if len(temp.keys()) > 1:
        log.error("unexpected format")
        return
    
    try:
        key = temp.keys()[0]
    except IndexError:
        log.error("unexpected format")
        return

    item = temp[key]
    log.debug("length: %s" % len(item))
    log.debug("result type: %s" % type(item))
    try:
        log.debug("item type: %s" % type(item[0]))
    except TypeError:
        log.error(item.keys())
    try:
        log.debug("buckets: %s" % item[0].keys())
    except TypeError:
        log.error("Invalid response (no keys): %s" %item[0])


# return wikipedia summary string of artist or 'nothing'
def get_good_bio(bios):
    for b in bios:    
        if str(b['site']) == 'wikipedia':
            return b['text']

    return 'Artist biography is not available.'


def inspect_context(context):
    try:
        for k, v in context.dicts[1].items():
            log.debug("key: %s" %(k))

            if isinstance(v, dict):
                log.debug("dict: %s" %(v.keys()))

            elif isinstance(v, list):
                log.debug("list = %s\n" %(len(v))) 

            elif isinstance(v, str) or isinstance(v, unicode):
                log.debug("str: \"%s\"\n" %(v if v else "{EMPTY}"))

            else:
                log.debug("typ: %s\n" %(type(v)))

    except IndexError:
        log.error("Invalid context.")


