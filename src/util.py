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


def inspect_response(response):
    """
    debug echo nest response 
    @response = request.get response
    """
    try:
        js = response.json()
    except ValueError, AttributeError:
        print "   ERROR: could not get json"
        return
        
    if js['response']['status']['code'] is not 0:
        print "   ERROR: %s" % js['response']['status']['message']
        return

    temp = js['response']
    del temp['status']
    if len(temp.keys()) > 1:
        print "   ERROR: unexpected format"
        return
    
    try:
        key = temp.keys()[0]
    except IndexError:
        print "   ERROR: unexpected format"
        return

    item = temp[key]
    print "==========EXAMINE RESPONSE=========="
    print "   length: %s" % len(item)
    print "   result type: %s" % type(item)
    try:
        print "   item type: %s" % type(item[0])
    except TypeError:
        print item.keys()
    print "   ================================================="
    print
    print "REQUEST ITEM,"
    try:
        print "   keys: %s" % item[0].keys()
    except TypeError:
        print "   wat: %s" %item[0]
    print "   ================================================="
    print


# return wikipedia summary string of artist or 'nothing'
def get_good_bio(bios):
    for b in bios:    
        if str(b['site']) == 'wikipedia':
            return b['text']

    return 'Artist biography is not available.'


# recipe from some site
def expand_keys(dictionary, ident = '', braces=1):
    """ Recursively prints nested dictionaries."""

    for key, value in dictionary.iteritems():
        if isinstance(value, dict):
            print '%s%s%s%s' %(ident,braces*'[',key,braces*']') 
            print_dict(value, ident+'  ', braces+1)
        else:
            print ident+'%s' %key


def inspect_context(context):
    try:
        for k, v in context.dicts[1].items():
            try:
                print " key: %s" %(k)

                if isinstance(v, dict):
                    print " val:",
                    for item in v.keys():
                        print "%s," %(item),
                    print
                elif isinstance(v, list):
                    print " typ: list"
                elif isinstance(v, str) or isinstance(v, unicode):
                    print " val: \"%s\"" %(v)
                else:
                    print " typ: %s" %(type(v))

                print " len: %s" %(len(v))
                print

            except TypeError:
                print " %s: %s" % (k, v)
    except IndexError:
        print "DEBUG: invalid context"


