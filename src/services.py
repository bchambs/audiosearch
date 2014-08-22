from __future__ import absolute_import

from audiosearch import config as cfg



class EchoNestService(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"


    def __init__(self, type_, method, resource_name, buckets=None):
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self.ttl = cfg.REDIS_TTL
        self.payload = {
            'api_key': cfg.API_KEY,
            'format': "json",
        }
        self.resource_name = resource_name
        self.dependency = None
        if buckets:
            self.payload['bucket'] = buckets


    def __str__(self):
        return "EchoNestService"


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


    def __init__(self, artist_name):
        super(ArtistProfile, self).__init__(self.TYPE_, self.METHOD, artist_name, self.BUCKETS)
        self.payload['name'] = artist_name


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


    def __init__(self, artist_name):
        super(ArtistSongs, self).__init__(self.TYPE_, self.METHOD, artist_name, self.BUCKETS)
        self.payload['artist'] = artist_name
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


    def __init__(self, artist_name):
        super(SimilarArtists, self).__init__(self.TYPE_, self.METHOD, artist_name, self.BUCKETS)
        self.payload['name'] = artist_name
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "SimilarArtists"




class SearchArtists(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'


    def __init__(self, query):
        super(SearchArtists, self).__init__(self.TYPE_, self.METHOD, query)
        self.payload['name'] = query
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


    def __init__(self, query, artist_name=None):
        super(SearchSongs, self).__init__(self.TYPE_, self.METHOD, query, self.BUCKETS)
        self.payload['title'] = query
        self.payload['artist'] = artist_name
        self.payload['results'] = cfg.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


    def __str__(self):
        return "SearchSongs"




# Used to acquire a song's Echo Nest id.
class SongID(SearchSongs):

    def __init__(self, song_title, artist_name):
        super(SongID, self).__init__(song_title, artist_name=artist_name)
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
    

    def __init__(self, artist_name, song_title=None):
        super(Playlist, self).__init__(self.TYPE_, self.METHOD, song_title or artist_name, self.BUCKETS)
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "Playlist"




class SongPlaylist(Playlist):
    def __init__(self, song_title, artist_name):
        super(SongPlaylist, self).__init__(self.TYPE_, self.METHOD, song_title, self.BUCKETS)
        self.payload['type'] = "song-radio"
        self.dependency = SongID(song_title, artist_name)


    def __str__(self):
        return "SongPlaylist"


    # Song playlists require an Echo Nest id to be used as a seed.
    def build(self, intermediate):
        try:
            self.payload['song_id'] = intermediate[0].get('id')

            if not self.payload['song_id']:
                raise EmptyServiceResponse()

        except IndexError:
            raise EmptyServiceResponse()




class ArtistPlaylist(Playlist):
    def __init__(self, artist_name):
        super(ArtistPlaylist, self).__init__(self.TYPE_, self.METHOD, artist_name, self.BUCKETS)
        self.payload['artist'] = artist_name
        self.payload['variety'] = 1
        self.payload['type'] = "artist-radio"


    def __str__(self):
        return "ArtistPlaylist"




class SongProfile(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'profile'
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        'song_type',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, song_title, artist_name):
        super(SongProfile, self).__init__(self.TYPE_, self.METHOD, song_title, self.BUCKETS)
        self.dependency = SongID(song_title, artist_name)


    def __str__(self):
        return "SongProfile"


    # Song playlists require an Echo Nest id.
    def build(self, intermediate):
        try:
            self.payload['song_id'] = intermediate[0].get('id')

            if not self.payload['song_id']:
                raise EmptyServiceResponse()

        except IndexError:
            raise EmptyServiceResponse()


    def trim(self, data):
        data = data[0]
        result = {}

        audio = data.get('audio_summary')

        if not audio: 
            raise EmptyServiceResponse()

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

        result['liveness'] = to_percent(audio.get('liveness'))
        result['danceability'] = to_percent(audio.get('danceability'))
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
        super(TopArtists, self).__init__(self.TYPE_, self.METHOD, "top_artists")
        self.payload['results'] = cfg.RESULTS


    def __str__(self):
        return "TopArtists"




class EchoNestServiceFailure(Exception):
    pass




class EmptyServiceResponse(Exception):
    pass




def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    if len(percent) > 0:
        return percent[0] + " %"
    else:
        return ''
