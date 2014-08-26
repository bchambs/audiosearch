from __future__ import absolute_import

from audiosearch.constants import API_KEY, N_SRVC_RESULTS



class ServiceError(Exception):
    pass

class EmptyResponseError(Exception):
    pass


class EchoNestService(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"
    payload = {
        'api_key': API_KEY,
        'format': "json",
    }


    def __init__(self, type_, method, buckets=None):
        self.dependency = None
        self.payload['bucket'] = buckets
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])


    def __str__(self):
        return "EchoNestService"


class ArtistProfileService(EchoNestService):
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


    def __init__(self, artist):
        super(ArtistProfileService, self).__init__(self.TYPE_, self.METHOD, 
            self.BUCKETS)
        self.payload['name'] = artist


    def __str__(self):
        return "ArtistProfileService"


    def process(self, raw_data):
        data = {}

        # Artist location.
        try:
            location_wrap = raw_data.pop('artist_location')
            data['location'] = location_wrap.pop('location')
        except KeyError:
            pass

        # Genre tags.
        try:
            genres = raw_data.pop('genres')
        except KeyError:
            pass
        else:
            genres = genres[:N_GENRE_TAGS]
            data['genres'] = []

            for genre in genres:
                data['genres'].append(genre['name'])

        # Years active.
        try:
            years_active_wrap = raw_data.pop('years_active')
            years_active = years_active_wrap.pop(0)
        except IndexError, KeyError:
            pass
        else:
            start = years_active.get('start', "Unknown")
            end = years_active.get('end', "Present")

            data['years_active'] = "(%s - %s)" %(start, end)

        # Image urls.
        try:
            image_wrap = raw_data.pop('images')
            image = image_wrap.pop(0)
            data['image'] = image.pop('url')
        except IndexError, KeyError:
            pass

        return data


class ArtistSongsService(EchoNestService):
    TYPE_ = 'playlist'
    METHOD = 'static'
    BUCKETS = [
        'audio_summary',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist):
        super(ArtistSongsService, self).__init__(self.TYPE_, self.METHOD, 
            self.BUCKETS)
        self.payload['artist'] = artist
        self.payload['results'] = N_SRVC_RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"


    def __str__(self):
        return "ArtistSongsService"


class SimilarArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'similar'
    BUCKETS = [
        'images',
        'terms',
        'songs',
    ]
    ECHO_NEST_KEY = 'artists'


    def __init__(self, artist):
        super(SimilarArtistsService, self).__init__(self.TYPE_, self.METHOD, 
            self.BUCKETS)
        self.payload['name'] = artist
        self.payload['results'] = N_SRVC_RESULTS


    def __str__(self):
        return "SimilarArtistsService"


class SearchArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'


    def __init__(self, artist_name):
        super(SearchArtistsService, self).__init__(self.TYPE_, self.METHOD)
        self.payload['name'] = artist_name
        self.payload['results'] = N_SRVC_RESULTS


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
            self.BUCKETS)
        self.payload['title'] = song
        self.payload['artist'] = artist
        self.payload['results'] = N_SRVC_RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


    def __str__(self):
        return "SearchSongsService"


# Used to acquire a song's Echo Nest id.
class SongID(SearchSongsService):

    def __init__(self, artist, song):
        super(SongID, self).__init__(song, artist)
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
    

    def __init__(self):
        super(Playlist, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.payload['results'] = N_SRVC_RESULTS


    def __str__(self):
        return "Playlist"


class SongPlaylistService(Playlist):
    def __init__(self, artist, song):
        super(SongPlaylistService, self).__init__()
        self.payload['type'] = "song-radio"
        self.dependency = SongID(song, artist)


    def __str__(self):
        return "SongPlaylistService"


    # Song playlists require an Echo Nest id to be used as a seed.
    def combine_dependency(self, intermediate):
        try:
            first_result = intermediate.pop(0)
            self.payload['song_id'] = first_result.pop('id')
        except IndexError, KeyError:
            raise EmptyResponseError()


class ArtistPlaylistService(Playlist):
    def __init__(self, artist):
        super(ArtistPlaylistService, self).__init__()
        self.payload['artist'] = artist
        self.payload['variety'] = 1
        self.payload['type'] = "artist-radio"


    def __str__(self):
        return "ArtistPlaylistService"


class SongProfileService(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'profile'
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        'song_type',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist, song):
        super(SongProfileService, self).__init__(self.TYPE_, self.METHOD, 
            self.BUCKETS)
        self.dependency = SongID(artist, song)


    def __str__(self):
        return "SongProfileService"


    # Song playlists require an Echo Nest id.
    def combine_dependency(self, intermediate):
        try:
            first_result = intermediate.pop(0)
            self.payload['song_id'] = first_result.pop('id')
        except IndexError, KeyError:
            raise EmptyResponseError()


    def process(self, data):
        data = data[0]
        result = {}

        audio = data.get('audio_summary')

        if not audio: 
            raise EmptyResponseError()

        try:
            t = audio.get('duration')
            result['duration'] = convert_seconds(t)
        except AttributeError, IndexError:
            pass

        result['liveness'] = to_percent(audio.get('liveness'))
        result['danceability'] = to_percent(audio.get('danceability'))
        result['tempo'] = "%s bpm" %audio.get('tempo')

        result['tracks'] = data.get('tracks')
        result['song_hotttnesss'] = data.get('song_hotttnesss')
        result['song_hotttnesss_rank'] = data.get('song_hotttnesss_rank')
        result['artist_foreign_ids'] = data.get('artist_foreign_ids')

        return result


# TODO: create scheduled service to update this.
class TopArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'top_hottt'
    BUCKETS = [
        'hotttnesss_rank',
    ]
    ECHO_NEST_KEY = 'artists'


    def __init__(self):
        super(TopArtistsService, self).__init__(self.TYPE_, self.METHOD, 
            self.BUCKETS)
        self.payload['results'] = N_SRVC_RESULTS


    def __str__(self):
        return "TopArtistsService"




# TODO: remove index error, move try to caller for None str
def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    try:
        s =  percent.pop(0) + " %"
    except IndexError:
        s =  ''

    return s




# Used to display (M:S) duration on song profile.
def convert_seconds(t):
    print "t is %s" %(type(t))
    print "t is %s" %(type(t))
    print "t is %s" %(type(t))
    print "t is %s" %(type(t))
    print "t is %s" %(type(t))
    time = str(t)
    minutes = time.split('.')[0]

    if len(minutes) > 1:
        m = int(minutes) / 60
        s = round(t - (m * 60))
        seconds = str(s).split('.')[0]

        if len(seconds) < 2:
            seconds = seconds + "0"

        return "(%s:%s)" %(m, seconds)
    else:
        return "(:%s)" %(minutes[0])






