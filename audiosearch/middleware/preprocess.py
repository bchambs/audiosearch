from __future__ import absolute_import
import urllib


class Normalizer(object):

    def process_view(self, request, view_func, view_args, view_kwargs):
        normal_GET = dict()
        normal_kwargs = dict()

        if request.GET:
            normal_GET = _normalize(request.GET.copy())

        if view_kwargs:
            normal_kwargs = _normalize(view_kwargs)

        return view_func(request, normal_GET, normal_kwargs)


def _normalize(d):
    normal = dict()

    for k, v in d.iteritems():
        if v:  # Why is an empty unicode str not None???
            try:
                normal[k] = _normalize_string(v)
            except AttributeError:
                normal[k] = v 

    return normal


# Convert string to lowercase, strip white space, and remove consecutive spaces.
def _normalize_string(value):
    normal = value.strip().lower()
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
