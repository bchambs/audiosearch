from __future__ import absolute_import

from audiosearch.models.service.base import EchoNestService


class Error(Exception):
    pass


class DependencyError(Error):
    pass


class SongID(EchoNestService):
    """Used to acquire a song's Echo Nest id."""
    TYPE_ = 'song'
    METHOD = 'search'
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist, song):
        payload = dict(results=1, song_type=None)
        super(SongID, self).__init__(SongID.TYPE_, SongID.METHOD, payload)


    def __repr__(self):
        tail = " (dependency)"
        return super(SongID, self).__repr__() + tail


    def build(self, response):
        pass


