from __future__ import absolute_import

from audiosearch.models.service.base import EchoNestService


class DependencyError(Exception):
    pass


class SongID(EchoNestService):
    """Used to acquire a song's Echo Nest id."""
    _type = 'song'
    _method = 'search'
    echo_key = 'songs'


    def __init__(self, artist, song):
        payload = dict(results=1, song_type=None)
        super(SongID, self).__init__(SongID._type, SongID._method, **payload)


    def __repr__(self):
        tail = " (dependency)"
        return super(SongID, self).__repr__() + tail
