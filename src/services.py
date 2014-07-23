from __future__ import absolute_import

from random import choice, sample
import datetime

import audiosearch.config as cfg
import src.util as util


class ENCall(object):
    """
    Abstract class representing input to request.get().
    """

    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"

    def __init__(self, type_, method, id_, buckets):
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self.id_ = id_
        self.payload = {
            'api_key': cfg.API_KEY,
            'format': "json",
        }
        if buckets:
            self.payload['bucket'] = buckets

        self.ttl = cfg.REDIS_TTL
        self.debug = True if cfg.CONSUMER_DEBUG else False

    def trim(self, data):
        return data


class ArtistProfile(ENCall):
    """
    Package representing all required data for an artist profile request from Echo Nest.
    """

    # REST data
    TYPE_ = "artist"
    METHOD = "profile"
    BUCKETS = [
        'biographies',
        'hotttnesss',
        'images',
        'terms',
        'hotttnesss_rank',
    ]

    # REDIS data
    CALL_KEY = 'artist'
    REDIS_KEY = 'profile'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_


    def trim(self, data):
        result = {}

        if 'name' in data:
            result['name'] = data['name']

        if 'images' in data:
            result['title_image'] = data['images'][0]['url']

        if 'terms' in data:
            result['terms'] = []

            for x in range(0,5):
                try:
                    result['terms'].append(data['terms'][x]['name'])
                except IndexError:
                    break

        return result


class Playlist(ENCall):
    """
    Package representing all required data for a playlist request from Echo Nest.
    """

    # REST data
    TYPE_ = "playlist"
    METHOD = "static"
    BUCKETS = [
        'song_hotttnesss',
    ]

    # REDIS data
    CALL_KEY = 'songs'
    REDIS_KEY = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['artist_id'] = id_
        self.payload['results'] = 100
        self.payload['sort'] = "song_hotttnesss-desc"

    def trim(self, data):
        for song in data:
            song['song_hotttnesss'] = int(round(song['song_hotttnesss'] * 100))
        return data


class SimilarArtists(ENCall):
    """
    Package representing all required data for a similar artists request from Echo Nest.
    """

    # REST data
    TYPE_ = "artist"
    METHOD = "similar"
    BUCKETS = [
        'images',
        'terms',
        'familiarity',
        'songs',
    ]

    # REDIS data
    CALL_KEY = 'artists'
    REDIS_KEY = 'similar'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_
        self.payload['results'] = 100


class ArtistSearch(ENCall):
    """
    Package representing all required data for an artist search request from Echo Nest.
    """

    # REST data
    TYPE_ = "artist"
    METHOD = "suggest"

    # REDIS data
    CALL_KEY = 'artists'
    REDIS_KEY = 'artists'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, None)
        self.payload['name'] = id_
        self.payload['results'] = 100


class SongSearch(ENCall):
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
        self.payload['results'] = 100
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


class SimilarSongs(SongSearch):
    """
    Package representing all required data for an similar songs request from Echo Nest.
    """

    REDIS_KEY = 'similar_songs' 


    def __init__(self, id_):
        SongSearch.__init__(self, id_)
        self.payload['type'] = 'song-radio'
        self.payload['song_id'] = id_

        del(self.payload['title'])


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
