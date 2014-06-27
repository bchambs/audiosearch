from __future__ import absolute_import
from random import choice
from pprint import pprint
import logging
import sys

import requests

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# examine value of string, dict, or list
def debug(s=None, d=None, l=None):
    if s:
        logging.debug(s)
    if d:
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


# remove unused data from artist profile json
# alter json keys to make client-side loading simpler
def process_artist(data):
    if 'biographies' in data:
        data['bio_full'] = trim_bios(data['biographies'])
        data['bio_trunc'] = data['bio_full'][:200]
        del data['biographies'] 

    if 'images' in data:
        data['title-image'] = data['images'][0]['url']

        data['images'] = data['images'][:4]
        for x in range(0,4):
            data['images'][x] = data['images'][x]['url']

    for x in data['images']:
        print x

    if 'terms' in data:
        try:
            if len(data['terms']) is 1:
                data['terms'] = data['terms'][0]['name']
            else:
                data['terms'] = data['terms'][0]['name'] + ', ' + data['terms'][1]['name']
        
        # CATCH handle the unlikely event that a term item exists without a name key
        except KeyError:
            debug(s='term without a name key, wow!')
            pass


# return wikipedia summary string of artist or 'nothing'
def trim_bios(bios):
    for b in bios:    
        if str(b['site']) == 'wikipedia':
            return b['text']

    return 'Artist biography is not available.'
