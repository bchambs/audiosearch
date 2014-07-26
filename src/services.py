from __future__ import absolute_import

from random import choice, sample
import datetime

import audiosearch.config as cfg
import src.util as util


class ENCall(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"

    def __init__(self, type_, method, id_, buckets=None):
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self.id_ = id_
        self.ttl = cfg.REDIS_TTL
        self.payload = {
            'api_key': cfg.API_KEY,
            'format': "json",
        }
        if buckets:
            self.payload['bucket'] = buckets

        self.debug = True if cfg.CONSUMER_DEBUG else False # TODO: remove

    def trim(self, data):
        return data


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


    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_

    def trim(self, data):
        result = {}

        result['name'] = data.get('name')
        result['genres'] = data.get('terms')[:5]

        city = data.get('artist_location').get('city')
        country = data.get('artist_location').get('country')

        if city and country:
            result['location'] = city + ", " + country
        elif country:
            result['location'] = country

        return result


class ArtistSongs(ENCall):
    TYPE_ = 'playlist'
    METHOD = 'static'
    CALL_KEY = 'songs'
    REDIS_KEY = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_)
        self.payload['artist_id'] = id_
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"


class SearchArtists(ENCall):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    CALL_KEY = 'artists'
    REDIS_KEY = 'artists'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_)
        self.payload['name'] = id_
        self.payload['results'] = cfg.RESULTS


class SearchSongs(ENCall):
    """
    Package representing all required data for an song search request from Echo Nest.
    """

    # REST data
    TYPE_ = "song"
    METHOD = "search"

    # REDIS data
    CALL_KEY = 'songs'
    REDIS_KEY = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, None)
        self.payload['title'] = id_
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


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
        self.payload['id'] = id_
        self.payload['results'] = cfg.RESULTS


class SimilarSongs(ENCall):
    TYPE_ = 'playlist'
    METHOD = 'static'
    CALL_KEY = 'songs'
    REDIS_KEY = 'similar_songs' 

# id=-AR633SY1187B9AC3B9
    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, None)
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        # self.payload['sort'] = "artist_familiarity-desc"
        self.payload['song_id'] = id_
        self.payload['type'] = "song-radio"


class SongProfile(ENCall):
    """
    Package representing all required data for an song profile request from Echo Nest.
    """

    # REST data
    TYPE_ = "song"
    METHOD = "profile"
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        # 'tracks'
    ]

    # REDIS data
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


class ENCallFailure(Exception):
    pass
