from random import choice, sample

import audiosearch.config as cfg
from src import utils


"""
resource = prefix + resource_id
resource_id = name of artist or song
content = resource's profile, similar_songs, etc
content_key = profile, similar_songs, etc
echo_key : key used to access resource from echo nest api
"""


class EchoNestService(object):
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


    def __str__(self):
        return "EchoNestService(base)"


    def trim(self, data):
        return data


    def build(self, intermediate):
        return 


class ArtistProfile(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'profile'
    BUCKETS = [
        'artist_location',
        'biographies',
        'images',
        'hotttnesss',
        'genre',
        'years_active',
    ]
    ECHO_NEST_KEY = 'artist'


    def __init__(self, resource_id):
        super(ArtistProfile, self).__init__(self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['name'] = resource_id


    def __str__(self):
        return "ArtistProfile"


    def trim(self, data):
        print self.url
        result = {}

        location_dict = data.get('artist_location')
        if location_dict:
            result['location'] = location_dict.get('location')

        genres = data.get('genres')
        if genres:
            genres = genres[:cfg.GENRE_COUNT]
            result['genres'] = []

            for genre in genres:
                result['genres'].append(genre['name'])

        years_active = data.get('years_active')
        if years_active:
            years_active = years_active[0]
            start = years_active.get('start', "Unknown")
            end = years_active.get('end', "Present")

            result['years_active'] = "(%s - %s)" %(start, end)

        images = data.get('images')
        if images:
            try:
                result['image'] = images[0]['url']
            except KeyError:
                pass

        return result


class ArtistSongs(EchoNestService):
    TYPE_ = 'playlist'
    METHOD = 'static'
    BUCKETS = [
        'audio_summary',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, resource_id):
        super(ArtistSongs, self).__init__(self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['artist'] = resource_id
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"


    def __str__(self):
        return "ArtistSongs"


class SimilarArtists(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'similar'
    BUCKETS = [
        'images',
        'terms',
        'songs',
    ]
    ECHO_NEST_KEY = 'artists'


    def __init__(self, resource_id):
        super(SimilarArtists, self).__init__(self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['name'] = resource_id
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "SimilarArtists"


class SearchArtists(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'


    def __init__(self, resource_id):
        super(SearchArtists, self).__init__(self.TYPE_, self.METHOD, resource_id)
        self.payload['name'] = resource_id
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "SearchArtists"


class SearchSongs(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'search'
    BUCKETS = [
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, resource_id, artist_id=None):
        super(SearchSongs, self).__init__(self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['title'] = resource_id
        self.payload['artist'] = artist_id
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


    def __str__(self):
        return "SearchSongs"


# this service exists to get the echo nest hash associated with a song given the title and artist name
class SongID(SearchSongs):

    def __init__(self, resource_id, artist_id):
        super(SongID, self).__init__(resource_id, artist_id=artist_id)
        self.payload['results'] = 1
        self.payload['song_type'] = None


    def __str__(self):
        return "SongID"


class Playlist(EchoNestService):
    TYPE_ = 'playlist'
    METHOD = 'static'
    BUCKETS = [
        'song_hotttnesss',
    ]
    ECHO_NEST_KEY = 'songs'
    

    # if artist_id is present, generate playlist with a song_id as the seed
    def __init__(self, resource_id, artist_id=None):
        super(Playlist, self).__init__(self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.payload['results'] = cfg.RESULTS

        if artist_id:
            self.payload['type'] = "song-radio"
            self.dependency = SongID(resource_id, artist_id)
        else:
            self.payload['artist'] = resource_id
            self.payload['variety'] = 1
            self.payload['type'] = "artist-radio"
        

    def __str__(self):
        return "Playlist"


    def build(self, intermediate):
        if intermediate:
            self.payload['song_id'] = intermediate[0].get('id')


class SongProfile(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'profile'
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        'song_type',
        # 'tracks',
        # 'id:7digital-US',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, resource_id, artist_id):
        super(SongProfile, self).__init__(self.TYPE_, self.METHOD, resource_id, self.BUCKETS)
        self.dependency = SongID(resource_id, artist_id)
        # self.payload['limit'] = True


    def __str__(self):
        return "SongProfile"


    def build(self, intermediate):
        if not intermediate: 
            artist = intermediate.get('artist_name')
            song = intermediate.get('title')
            raise DependencyFailure("Unable to find information for artist:%s , song:%s") %(artist, song)

        self.payload['id'] = intermediate[0].get('id')


    def trim(self, data):
        data = data[0]
        result = {}

        audio = data.get('audio_summary')

        if not audio: return result

        # convert song duration, letter = float, word = string
        try:
            t = audio['duration']
            time = str(t)
            minutes = time.split('.')[0]

            if len(minutes) > 1:
                m = int(minutes) / 60
                s = round(t - (m * 60))
                seconds = str(s).split('.')[0]

                if len(seconds) < 2:
                    seconds = seconds + "0"

                result['duration'] = "(%s:%s)" %(m, seconds)
            else:
                result['duration'] = "(:%s)" %(minutes[0])
        except KeyError, IndexError:
            pass

        result['liveness'] = utils.to_percent(audio.get('liveness'))
        result['danceability'] = utils.to_percent(audio.get('danceability'))
        result['tempo'] = "%s bpm" %audio.get('tempo')

        result['tracks'] = data.get('tracks')
        result['song_hotttnesss'] = data.get('song_hotttnesss')
        result['song_hotttnesss_rank'] = data.get('song_hotttnesss_rank')
        result['artist_foreign_ids'] = data.get('artist_foreign_ids')

        return result


class TopArtists(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'top_hottt'

    ECHO_NEST_KEY = 'artists'


    def __init__(self):
        super(TopArtists, self).__init__(self.TYPE_, self.METHOD, None)
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "TopArtists"


class TopSongs(SearchSongs):

    def __init__(self):
        super(TopSongs, self).__init__(self.TYPE_, None)
        self.payload['song_type'] = None


    def __str__(self):
        return "TopSongs"


class EchoNestServiceFailure(Exception):
    pass

class EmptyServiceResponse(Exception):
    pass


