from __future__ import absolute_import

from audiosearch.services.base import EchoNestService


class SearchArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'


    def __init__(self, artist):
        super(SearchArtistsService, self).__init__(self.TYPE_, self.METHOD)
        self.payload['name'] = artist

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


    def __init__(self, song, artist=None):
        super(SearchSongsService, self).__init__(self.TYPE_, self.METHOD, 
            buckets=self.BUCKETS)
        self.payload['title'] = song
        self.payload['artist'] = artist
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"

    def __str__(self):
        return "SearchSongsService"
