from __future__ import absolute_import

from audiosearch.handlers import miss

_DEFAULT_TTL = 3000     # In seconds.
_ID_SEPARATOR = '_'
_KEY_SEPARATOR = '::'


def build_template_map(content):
    


class Resource(object):
    _ttl = _DEFAULT_TTL

    def __init__(self, head, tail, name):
        id_ = _ID_SEPARATOR.join([head, tail])
        self._key = _KEY_SEPARATOR.join([id_, name])

    @property
    def key(self):
        return self._key

    @property
    def ttl(self):
        return self._ttl

    def handle_miss(self):
        return miss.get_echo_nest_data(self.key, self.ttl, self._build_service)



