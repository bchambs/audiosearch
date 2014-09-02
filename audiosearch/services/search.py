from __future__ import absolute_import

from audiosearch.services.base import EchoNestService


class SearchArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'


    def __init__(self, artist):
        payload = dict(name=artist)
        super(SearchArtistsService, self).__init__(self.TYPE_, self.METHOD, 
            payload)

    def __str__(self):
        return "SearchArtistsService"


class SearchSongsService(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'search'
    BUCKETS = [
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist, song):
        payload = {
            'artist': artist,
            'bucket': SearchSongsService.BUCKETS,
            'song_type': "studio",
            'sort': "song_hotttnesss-desc",
            'title': song,
        }
        super(SearchSongsService, self).__init__(self.TYPE_, self.METHOD, 
            payload)

    def __str__(self):
        return "SearchSongsService"
