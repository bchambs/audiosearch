"""
template dict

resource:
    name: string
    div_id: str(resource)
    title: header text
    nav: 'page' or 'more'
    data: {
        paged dict
    }
"""
from __future__ import absolute_import

_DEFAULT_TTL = 3000     # In seconds.


class BaseResource(object):
    _separator = '::'
    ttl = _DEFAULT_TTL


    def __init__(self, prefix, name):
        self.key = _separator.join([prefix, name])
