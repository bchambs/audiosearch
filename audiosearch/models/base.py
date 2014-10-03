from __future__ import absolute_import

from audiosearch.utils.decorators import stdout_gap


# Key format constants
PREFIX_SEP = ':'
KEY_SEP = '::'

# String used for resources without 'names' (eg top hottt)
DEFAULT_ALIAS = '$'


def make_key(group, method, alias):
    """Key format, `GROUP:METHOD::alias`."""
    prefix = PREFIX_SEP.join([group, method])
    return KEY_SEP.join([prefix, alias])


class EchoNestResource(object):
    def __init__(self, *args):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        
        # Map *args to _fields
        for field, value in zip(self._fields, args):
            setattr(self, field, value)

        self._key = make_key(self.group, self.method, self.alias)
        self._template_key = self.method


    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key

    def __hash__(self):
        return hash(self.key)


    @classmethod
    def from_scheme(cls, **params):
        args = [params.get(field) for field in cls._fields]
        return cls(*args)


    @property
    def key(self):
        return self._key

    @property
    def template_key(self):
        return self._template_key


    def get_scheme(self):
        scheme = {}

        for field in self._fields:
            scheme[field] = getattr(self, field)
        return scheme

    def clean(self, data):
        return data
