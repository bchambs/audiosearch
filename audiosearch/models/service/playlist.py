from __future__ import absolute_import

from audiosearch.services import dependency
from audiosearch.services.base import EchoNestService


class PlaylistBase(EchoNestService):
    TYPE_ = 'playlist'
    METHOD = 'static'
    BUCKETS = [
        'song_hotttnesss',
    ]
    ECHO_NEST_KEY = 'songs'
    

    def __init__(self, payload, **kwargs):
        super(PlaylistBase, self).__init__(self.TYPE_, self.METHOD, payload,
            **kwargs)


class SongPlaylist(PlaylistBase):
    BUCKETS = [
        'audio_summary',
    ]

    def __init__(self, artist, song):
        buckets = PlaylistBase.BUCKETS + SongPlaylistService.BUCKETS
        payload = dict(type='song-radio', bucket=buckets)
        dependencies = list(dependency.SongID(song, artist))

        super(SongPlaylistService, self).__init__(payload, 
            dependencies=dependencies)


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

