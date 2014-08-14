import json
import urllib

from django.http import HttpResponse

from audiosearch.settings import DEBUG as DJANGO_DEBUG


class AudiosearchDebug(object):

    def process_request(self, request):
        if request.is_ajax():
            if not request.GET.get('resource_id') and not request.GET.get('content_key'):
                return HttpResponse(json.dumps({}), content_type="application/json")

    def process_view(self, request, view_func, view_args, view_kwargs):
        if DJANGO_DEBUG and not request.is_ajax():
            view_kwargs['debug'] = True

        if 'artist' in view_kwargs:
            artist = urllib.unquote_plus(view_kwargs['artist'])
            view_kwargs['artist'] = artist.strip()

        if 'song' in view_kwargs:
            song = urllib.unquote_plus(view_kwargs['song'])
            view_kwargs['song'] = song.strip()

