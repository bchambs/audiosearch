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

