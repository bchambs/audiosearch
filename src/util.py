from __future__ import absolute_import
from random import choice, sample
import logging
import sys
import ast


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from audiosearch.settings import MORE_RESULTS

def page_resource(page, resource):
    result = {}
    paginator = Paginator(resource, MORE_RESULTS)

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
    paged_resource = page_resource(page, resource) # TODO: this is ridiculous, rename something
    result[rtype] = paged_resource.object_list
    result['has_next'] = True if paged_resource.has_next else False
    result['has_previous'] = True if paged_resource.has_previous else False
    result['current_page'] = paged_resource.number
    result['total_pages'] = paged_resource.paginator.num_pages

    try:
        result['previous_page_number'] = paged_resource.previous_page_number()
    except EmptyPage:
        pass
    try:
        result['next_page_number'] = paged_resource.next_page_number()
    except EmptyPage:
        pass

    return result

# examine value of string, dict, or list
def debug(s=None, d=None, keys=None, values=None, l=None):
    if s:
        logging.debug(s)
    if d:
        if keys:
            for k in d:
                logging.debug(k)
        elif values:
            for v in d.items():
                logging.debug(v)
        else:
            for k, v in d.items():
                logging.debug('k: %s, v: %s' % (k, v))
    if l:
        for i in l:
            logging.debug(i)

def debug_subtitle(s):
    logging.debug('')
    logging.debug(':::::::%s' % s)
    logging.debug('')

def debug_title(s):
    logging.debug('####################################################')
    logging.debug('                %s' % s)
    logging.debug('####################################################')


# return wikipedia summary string of artist or 'nothing'
def get_good_bio(bios):
    for b in bios:    
        if str(b['site']) == 'wikipedia':
            return b['text']

    return 'Artist biography is not available.'


def remove_duplicate_songs (data, n):
    trunc = []
    comparisons = {}
    
    for song in data:
        s = song['title'].lower()
        
        if s not in comparisons:
            comparisons[s] = 1
            trunc.append(song['title'])

        if len(trunc) is n:
            break

    return trunc
