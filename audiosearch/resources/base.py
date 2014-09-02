from __future__ import absolute_import


_DEFAULT_TTL = 3000     # In seconds.
_ID_SEPARATOR = '_'
_KEY_SEPARATOR = '::'


class BaseResource(object):
    _ttl = _DEFAULT_TTL

    def __init__(self, head, tail, name):
        self._id_ = _ID_SEPARATOR.join([head, tail])
        self._name = name
        self._key = _KEY_SEPARATOR.join([self._id_, name])

    @property
    def id(self):
        return self._id_

    @property
    def key(self):
        return self._key

    @property
    def name(self):
        return self._name

    @property
    def ttl(self):
        return self._ttl



