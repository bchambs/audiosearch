from __future__ import absolute_import
import urllib


class Normalizer(object):
    """Convert request data to standardized format.  Django request.GET is
    immutable in a normal request/response cycle so pass a new formatted dict
    to views.

    Current format:
        1. No leading or trailing white space.
        2. Lowercase.
        3. '+' converted to space.
        4. No consecutive spaces.
        5. Empty strings are set to NoneType.

    TODO: preserve kwarg values' case in a second dict or dict of 
        namedtuple(normalize, original)
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        normal_GET = {}
        normal_kwargs = {}

        if request.GET:
            normal_GET = _normalize(request.GET.copy())

        if view_kwargs:
            normal_kwargs = _normalize(view_kwargs)

        return view_func(request, normal_GET, **normal_kwargs)


def _normalize(d):
    """Return a new dict with normalized values."""

    normal = {}

    for k, v in d.iteritems():
        if v:
            try:
                normal[k] = _normalize_string(v)
            except AttributeError:
                normal[k] = v 
        else:
            normal[k] = None    # TODO: see why empty unicode strs do not throw. 
                                # --> see if unicode has strip(), lower()... etc

    return normal


# Convert string to lowercase, strip white space, and remove consecutive spaces.
def _normalize_string(s):
    stripped = s.strip()
    lowered = stripped.lower()
    spacey = urllib.unquote_plus(lowered)
    return ' '.join(spacey.split())


# Remove escaping from ajax requests.
# TODO: see if I can remove this.
def _unescape_html(s):
    s = s.replace("&lt;", "<")
    s = s.replace("&gt;", ">")
    s = s.replace("&amp;", "&")
    s = s.replace("&#39;", "'")

    return s
