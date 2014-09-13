from __future__ import absolute_import

from audiosearch.models.service.dependency import SongID
from audiosearch.models.service.base import EchoNestService


class PlaylistBase(EchoNestService):
    _type = 'playlist'
    _method = 'static'
    _buckets = [
        'song_hotttnesss',
    ]
    ECHO_NEST_KEY = 'songs'
    

    def __init__(self, payload, **kwargs):
        super(PlaylistBase, self).__init__(PlaylistBase._type, 
                                            PlaylistBase._method, payload, 
                                            **kwargs)


class SongPlaylist(PlaylistBase):
    _buckets = [
        'audio_summary',
    ]

    def __init__(self, artist, song):
        buckets = PlaylistBase._buckets + SongPlaylist._buckets
        payload = dict(type='song-radio', bucket=buckets)
        req = SongID(song, artist)

        super(SongPlaylist, self).__init__(payload, 
            dependency=req)


    # def combine_dependency(self, intermediate):
    #     try:
    #         first_result = intermediate.pop()
    #         self.payload['song_id'] = first_result.pop('id')
    #     except (IndexError, KeyError):
    #         raise EmptyResponseError()


class ArtistPlaylist(PlaylistBase):

    def __init__(self, artist):
        payload = dict(artist=artist, variety=1, type='artist-radio')
        super(ArtistPlaylistService, self).__init__(payload)

