from __future__ import absolute_import


_DEFAULT_TTL = 3000     # In seconds.

_ARTIST_SONG_SEP = ' BY '
_ID_SEP = '_'
_KEY_SEP = '::'


class BaseResource(object):
    _ttl = _DEFAULT_TTL

    def __init__(self, head, tail, name):
        self._id_ = _ID_SEP.join([head, tail])
        self._key = _KEY_SEP.join([self._id_, name])

    @property
    def id(self):
        return self._id_

    @property
    def key(self):
        return self._key

    @property
    def ttl(self):
        return self._ttl

    @staticmethod
    def _song_by_artist(artist, song):
        return _ARTIST_SONG_SEP.join([song, artist])

