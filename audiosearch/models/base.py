from __future__ import absolute_import

# Key format constants
PREFIX_SEP = ':'
KEY_SEP = '::'


def make_key(group, method, name):
    """Cache key format, 'GROUP:METHOD::name'"""
    prefix = PREFIX_SEP.join([group, method])
    return KEY_SEP.join([prefix, name])


class BaseResource(object):
    def __init__(self, group, method, name):
        key = make_key(group, method, name)

        self.group = group
        self.key = key
        self.method = method
        self.name = name
