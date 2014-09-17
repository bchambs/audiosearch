from __future__ import absolute_import

from audiosearch.models.service.dependency import SongID
from audiosearch.models.service.base import EchoNestService


class BasePlaylist(EchoNestService):
    _type = 'playlist'
    _method = 'static'
    _buckets = [
        'song_hotttnesss',
    ]
    ECHO_NEST_KEY = 'songs'
    

    def __init__(self, params):
        super(BasePlaylist, self).__init__(BasePlaylist._type, 
                                            BasePlaylist._method, **params)


class SongPlaylist(BasePlaylist):
    _buckets = [
        'audio_summary',
    ]


    def __init__(self, artist, song):
        buckets = BasePlaylist._buckets + SongPlaylist._buckets
        payload = dict(type='song-radio', bucket=buckets)
        super(SongPlaylist, self).__init__(payload)
        id_service = SongID(song, artist)
        self.dependencies.append(id_service)


    # def combine_dependency(self, intermediate):
    #     try:
    #         first_result = intermediate.pop()
    #         self.payload['song_id'] = first_result.pop('id')
    #     except (IndexError, KeyError):
    #         raise EmptyResponseError()


class ArtistPlaylist(BasePlaylist):

    def __init__(self, artist):
        payload = dict(artist=artist, variety=1, type='artist-radio')
        super(ArtistPlaylist, self).__init__(payload)

