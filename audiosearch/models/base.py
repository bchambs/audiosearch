from __future__ import absolute_import


# Key format constants
PREFIX_SEP = ':'
KEY_SEP = '::'


def make_key(group, method, name):
    """Cache key format, 'GROUP:METHOD::name'"""
    prefix = PREFIX_SEP.join([group, method])
    return KEY_SEP.join([prefix, name])


class EchoNestResource(object):
    def __init__(self, group, method, alias='$'):
        key = make_key(group, method, alias)

        self._key = key
        self._params = {}
        self.alias = alias
        self.group = group
        self.method = method

    @classmethod
    def from_scheme(cls, **params):
        args = [params.get(field) for field in cls._fields]
        return cls(*args)

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key

    def __hash__(self):
        return hash(self.key)

    @property
    def key(self):
        return self._key

    @property
    def params(self):
        return self._params
