from random import choice, sample
import datetime

import audiosearch.config as cfg
from src import utils


"""
resource = prefix + resource_id
resource_id = name of artist or song
content = resource's profile, similar_songs, etc
content_key = profile, similar_songs, etc
echo_key : key used to access resource from echo nest api
"""
class ENCall(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"


    def __init__(self, type_, method, resource_id, buckets=None):
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self.ttl = cfg.REDIS_TTL
        self.payload = {
            'api_key': cfg.API_KEY,
            'format': "json",
        }
        self.resource_id = resource_id
        self.dependency = None
        if buckets:
            self.payload['bucket'] = buckets


    def trim(self, data):
        return data


    def build(self, intermediate):
        return 


    def __str__(self):
        return "service.encall"


class ArtistProfile(ENCall):
    TYPE_ = 'artist'
    METHOD = 'profile'
    BUCKETS = [
        'terms',
        'artist_location',
        'years_active',
    ]
    ECHO_NEST_KEY = 'artist'
    CONTENT_KEY = 'profile'


    def __init__(self, resource_id):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['name'] = resource_id


    def trim(self, data):
        result = {}

        result['name'] = data.get('name')
        result['genres'] = data.get('terms')[:cfg.GENRE_COUNT]
        location = data.get('artist_location')

        if location:
            city = location.get('city')
            country = location.get('country') 

            if city and country:
                result['location'] = city + ", " + country
            elif country:
                result['location'] = country

        return result


    def __str__(self):
        return "service.artist profile"


class ArtistSongs(ENCall):
    TYPE_ = 'playlist'
    METHOD = 'static'
    ECHO_NEST_KEY = 'songs'
    CONTENT_KEY = 'songs'


    def __init__(self, resource_id):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id)
        self.payload['artist'] = resource_id
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"


    def __str__(self):
        return "service.artist songs"


class SearchArtists(ENCall):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'
    CONTENT_KEY = 'artists'


    def __init__(self, resource_id):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id)
        self.payload['name'] = resource_id
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "service.search artists"


class SearchSongs(ENCall):
    TYPE_ = 'song'
    METHOD = 'search'
    ECHO_NEST_KEY = 'songs'
    CONTENT_KEY = 'songs'


    def __init__(self, artist_id, resource_id, for_id=False):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id)
        self.for_id = for_id
        self.payload['title'] = resource_id
        self.payload['artist'] = artist_id
        self.payload['results'] = 1 if for_id else cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


    def __str__(self):
        return "service.search songs"


class SimilarArtists(ENCall):
    TYPE_ = 'artist'
    METHOD = 'similar'
    BUCKETS = [
        'images',
        'terms',
        'songs',
    ]
    ECHO_NEST_KEY = 'artists'
    CONTENT_KEY = 'similar_artists'


    def __init__(self, resource_id):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['name'] = resource_id
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "service.artist similar artists"


class SimilarSongs(ENCall):
    TYPE_ = 'playlist'
    METHOD = 'static'
    ECHO_NEST_KEY = 'songs'
    CONTENT_KEY = 'similar_songs' 


    def __init__(self, resource_id, resource_type, artist_id=None, song_id=None):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id)
        self.payload['results'] = cfg.RESULTS
        
        if resource_type == "artist":
            self.payload['artist'] = resource_id
        else:
            self.dependency = SearchSongs(artist_id, resource_id, for_id=True)


    def build(self, intermediate):
        if not intermediate: return None

        self.payload['song_id'] = intermediate[0].get('id')
        return 


    def __str__(self):
        return "service.artist similar songs"


class SongProfile(SearchSongs):
    TYPE_ = 'song'
    METHOD = 'profile'
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
    ]
    ECHO_NEST_KEY = 'songs'
    CONTENT_KEY = 'profile'


    def __init__(self, artist_id, resource_id):
        ENCall.__init__(self, self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.dependency = SearchSongs(artist_id, resource_id, for_id=True)


    def build(self, intermediate):
        if not intermediate: return None

        self.payload['id'] = intermediate[0].get('id')
        return 


    def __str__(self):
        return "service.song profile"


class ENCallFailure(Exception):
    pass
