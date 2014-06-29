from __future__ import absolute_import
from random import choice, sample
import logging
import sys

import requests

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

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


# remove unused data from artist profile json
# alter json keys to make client-side loading simpler
# TODO: remove all unused / trim everything
def process_artist(data):
    if 'biographies' in data:
        # displayed in modal
        data['bio_full'] = get_good_bio(data['biographies'])

        # summary: get first paragraph, if not optimal take first 400 letters
        paragraphs = data['bio_full'].split("\n")

        if len(paragraphs[0]) < 200 or len(paragraphs[0]) > 500:
            data['bio_trunc'] = data['bio_full'][:500]
        else:
            data['bio_trunc'] = paragraphs[0]

        del data['biographies'] 

    # banner images, take top 4 images, create (id, url) tuple, append to tiles key
    if 'images' in data:
        # data['tiles'] = []

        # for x in range(0,4):
        #     tup = 'tile-image-' + str(x + 1), data['images'][x]['url']
        #     data['tiles'].append(tup)
        data['tiles'] = []
        temp = sample(data['images'], 4)

        for x in range(0, len(temp)):
            tup = 'tile-image-' + str(x + 1), temp[x]['url']
            data['tiles'].append(tup)


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

    if 'hotttnesss' in data:
        data['hotttnesss'] = int(round(data['hotttnesss'] * 100))


# return wikipedia summary string of artist or 'nothing'
def get_good_bio(bios):
    for b in bios:    
        if str(b['site']) == 'wikipedia':
            return b['text']

    return 'Artist biography is not available.'
