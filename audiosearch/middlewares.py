from __future__ import absolute_import

import json
import urllib

from django.http import HttpResponse

from audiosearch.settings import DEBUG as DJANGO_DEBUG
from src import utils


class AudiosearchPreprocessor(object):

    def process_request(self, request):

        # Return empty object for empty requests.
        if request.is_ajax():
            if not request.GET.get('resource_id') and not request.GET.get('content_key'):
                return HttpResponse(json.dumps({}), content_type="application/json")

    def process_view(self, request, vfunc, vargs, vkwargs):

        # Normalize all query parameters.
        if len(request.GET) > 0:
            for param in request.GET:
                vkwargs[param] = normalize(param)

        # Create resource_id from 'cache_prefix' determined in urls.py
        prefix = vkwargs.get('cache_prefix')

        # Cache key separator.
        separator = ''

        if not prefix:
            pass

        # elif prefix == "top":

        # elif prefix == "trending":

        # elif prefix == "search":

        # elif prefix == "song":

        # elif prefix == "song":

        # elif prefix == "artist":






        # if 'artist' in vkwargs:
        #     artist = urllib.unquote_plus(vkwargs['artist'])
        #     vkwargs['artist'] = artist.strip()

        # if 'song' in vkwargs:
        #     song = urllib.unquote_plus(vkwargs['song'])
        #     vkwargs['song'] = song.strip()







        # Enable redis clear debug button.
        # if DJANGO_DEBUG and not request.is_ajax():
        #     vkwargs['debug'] = True
