from __future__ import absolute_import
from random import choice, sample
import logging
import sys


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