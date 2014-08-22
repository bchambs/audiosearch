from __future__ import absolute_import

import json
import urllib

from django.http import HttpResponse


class AudiosearchPreprocessor(object):

    # def process_request(self, request):

        # Normalize 

        





        # Return nothing for empty requests.
        # if request.is_ajax():
        #     resource_id = request.GET.get('resource_id')


        #         return HttpResponse(json.dumps({}), content_type="application/json")






    def process_view(self, request, vfunc, vargs, vkwargs):
        if  request.is_ajax():
            print vargs
            print vargs
            print vargs
            print vargs
        else:
            # sanitize artist and song in kwargs

            # sanitize prefix and resource_id in async

            # Create resource_id from 'cache_prefix' determined in urls.py.
            if request.is_ajax():
                prefix = vkwargs.get('prefix')
            else:
                prefix = vkwargs.get('cache_prefix')
            separator = ':#:'

            if not prefix:
                pass

            # top:#:music
            elif prefix == "top":
                resource_name = "music"
                vkwargs['resource_id'] = prefix + separator + resource_name

            # elif prefix == "trending":

            # elif prefix == "search":

            # elif prefix == "song":

            # elif prefix == "artist":


            
            # Normalize all query parameters.  Javascript strings must be unescaped (?).
            if len(request.GET) > 0:
                if request.is_ajax():
                    for param in request.GET:
                        un_param = unescape_html(param) 
                        vkwargs[param] = normalize(un_param)
                else:
                    for param in request.GET:
                        vkwargs[param] = normalize(param)


            # if 'artist' in vkwargs:
            #     artist = urllib.unquote_plus(vkwargs['artist'])
            #     vkwargs['artist'] = artist.strip()

            # if 'song' in vkwargs:
            #     song = urllib.unquote_plus(vkwargs['song'])
            #     vkwargs['song'] = song.strip()



# Attempt to convert item to lowercase, strip white space,
# and remove consecutive spaces.
def normalize(item):
    try:
        normal = item.strip().lower()
        normal = ' '.join(normal.split())
    except AttributeError:
        normal = item

    return normal



def unescape_html(s):
    if s:
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&amp;", "&")
        s = s.replace("&#39;", "'")

    return s
