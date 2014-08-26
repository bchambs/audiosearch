from __future__ import absolute_import
import json
import urllib

from django.http import HttpResponse


class Normalizer(object):

    # Normalize kwargs and query parameters.  
    # Store normal query params in kwargs.
    def process_view(self, request, vfunc, vargs, vkwargs):

        # Kwargs.
        if len(vkwargs):
            for k, v in vkwargs.items():
                try:
                    vkwargs[k] = _normalize(v)
                except AttributeError:
                    vkwargs[k] = v 

        # Query parameters.  Javascript strings (from ajax) must be unescaped (?).
        if len(request.GET):
            for k, v in request.GET.items():
                try:
                    # un_param = _unescape_html(param) 
                    # vkwargs[param] = _normalize(un_param)
                    vkwargs[k] = _normalize(v)
                except AttributeError:
                    vkwargs[k] = v


# Convert item to lowercase, strip white space, and remove consecutive spaces.
def _normalize(item):
    normal = item.strip().lower()
    normal = urllib.unquote_plus(normal)
    return ' '.join(normal.split())


# Remove escaping from ajax requests.
# TODO: see if I can remove this.
def _unescape_html(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&#39;", "'")

    return s
