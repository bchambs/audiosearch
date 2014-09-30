from __future__ import absolute_import
import urllib


def normalize(d):
    """Return a 'copy' of d with normalized values."""

    normal = {}

    for k, v in d.iteritems():
        try:
            normal[k] = clean(v)
        except TypeError:
            normal[k] = v

    return normal


def clean(s):
    """Strip white space, convert to lowercase, and remove consecutive spaces."""
    if not len(s):
        return None

    trimmed = s.strip()
    lowered = trimmed.lower()
    spacey = urllib.unquote_plus(lowered)
    return ' '.join(spacey.split())


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
            normal_GET = normalize(request.GET.copy())

        if view_kwargs:
            normal_kwargs = normalize(view_kwargs)

        page = int(normal_GET.get('page', 1))

        return view_func(request, normal_GET, page, **normal_kwargs)
