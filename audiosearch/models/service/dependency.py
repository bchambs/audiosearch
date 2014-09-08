from __future__ import absolute_import
import logging

from audiosearch.services.base import (EchoNestService, EmptyResponseError, 
    ServiceError)


logger = logging.getLogger("general_logger")


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
        super(SongID, self).__init__(self.TYPE_, self.METHOD, payload)

    def __repr__(self):
        tail = " (dependency)"
        return super(SongID, self).__repr__(tail)


    def build(self, response):
        try:
            first_result = response.pop()
        except IndexError:
            raise EmptyResponseError()
        else:
            try:
                id_ = first_result.pop('id')
            except KeyError:
                raise ServiceError("Missing required service field.")
            else:
                return dict(song_id=id_)


