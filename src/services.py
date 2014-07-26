from __future__ import absolute_import

from random import choice, sample
import datetime

import audiosearch.config as cfg
import src.util as util


class ENCall(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"

    def __init__(self, type_, method, call_id, buckets=None):
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self.call_id = call_id
        self.ttl = cfg.REDIS_TTL
        self.payload = {
            'api_key': cfg.API_KEY,
            'format': "json",
        }
        if buckets:
            self.payload['bucket'] = buckets

    def trim(self, data):
        return data


    def __str__(self):
        return "service.encall"


class ArtistProfile(ENCall):
    TYPE_ = 'artist'
    METHOD = 'profile'
    BUCKETS = [
        # 'images',
        'terms',
        'artist_location',
        'years_active',
    ]
    CALL_KEY = 'artist'
    REDIS_KEY = 'profile'


    def __init__(self, name):
        ENCall.__init__(self, self.TYPE_, self.METHOD, name, self.BUCKETS)
        self.payload['name'] = name

    def trim(self, data):
        result = {}

        result['name'] = data.get('name')
        result['genres'] = data.get('terms')[:cfg.GENRE_COUNT]

        city = data.get('artist_location').get('city')
        country = data.get('artist_location').get('country')

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
    CALL_KEY = 'songs'
    REDIS_KEY = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_)
        self.payload['artist'] = id_
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"


    def __str__(self):
        return "service.artist songs"


class SearchArtists(ENCall):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    CALL_KEY = 'artists'
    REDIS_KEY = 'artists'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_)
        self.payload['name'] = id_
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "service.search artists"


class SearchSongs(ENCall):
    TYPE_ = "song"
    METHOD = "search"
    CALL_KEY = 'songs'
    REDIS_KEY = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, None)
        self.payload['title'] = id_
        self.payload['results'] = cfg.RESULTS
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
    CALL_KEY = 'artists'
    REDIS_KEY = 'similar_artists'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['name'] = id_
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "service.artist similar artists"


class SimilarSongs(ENCall):
    TYPE_ = 'playlist'
    METHOD = 'static'
    CALL_KEY = 'songs'
    REDIS_KEY = 'similar_songs' 


    def __init__(self, id_, page):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_)
        self.payload['results'] = cfg.RESULTS
        if page == "artist":
            self.payload['artist'] = id_
        else:
            self.payload['song_id'] = id_


    def __str__(self):
        return "service.artist similar songs"


class SongProfile(ENCall):
    TYPE_ = "song"
    METHOD = "profile"
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        # 'tracks'
    ]
    CALL_KEY = 'songs'
    REDIS_KEY = 'profile'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_


    def trim(self, data):
        # song search returns a list. we're using an id so we'll always use the first item
        if len(data) == 0:
            return data
        else:
            data = data[0]

        result = {}

        if 'title' in data:
            result['title'] = data['title']

        if 'artist_name' in data:
            result['artist_name'] = data['artist_name']

        if 'artist_id' in data:
            result['artist_id'] = data['artist_id']
            
        if 'audio_summary' in data:
            result['audio_summary'] = data['audio_summary']

            song_duration = data['audio_summary']['duration'] / 60
            song_duration = str(round(song_duration,2))
            song_duration = song_duration.replace('.', ':')

            result['duration'] = song_duration

        if 'song_hotttnesss_rank' in data:
            result['rank'] = data['song_hotttnesss_rank']

        if 'song_hotttnesss' in data:
            result['hotttnesss'] = int(round(data['song_hotttnesss'] * 100))

        return result


    def __str__(self):
        return "service.song profile"


class ENCallFailure(Exception):
    pass
