"""
TODO: content.py assigns ttl, this should be determined by service class.
TODO: have ttl be determined by resource popularity with a tier system.
    1. top 5%, ttl = 6000 seconds
    2. next 30%, ttl = 3000 seconds
    3. rest, ttl = 2000
"""

from __future__ import absolute_import

from collections import namedtuple

DepMap = namedtuple('DepMap', 'service fields')

_API_KEY = 'QZQG43T7640VIF4FN'
_N_GENRE_TAGS = 5


class ServiceError(Exception):
    pass


class EmptyResponseError(Exception):
    pass


class EchoNestService(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"
    _FORMAT = 'json'
    _RESULT_MAX_LEN = 100   # Largest size result for Echo Nest responses.


    def __init__(self, type_, method, payload, **kwargs):
        self._dependencies = kwargs.get('dependencies')
        self._url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self._payload = {
            'api_key': _API_KEY,
            'format': EchoNestService._FORMAT,
            'bucket': kwargs.get('buckets'),
        }
        self._payload.update(payload)

    def __str__(self):
        return "EchoNestService"

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def payload(self):
        return self._payload

    @property
    def url(self):
        return self._url


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
        payload = dict(name=artist)
        print payload
        super(ArtistProfileService, self).__init__(self.TYPE_, self.METHOD, 
            payload, buckets=self.BUCKETS)
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
            data['genres'] = []

            for genre in genres[:_N_GENRE_TAGS]:
                data['genres'].append(genre['name'])

        # Years active.
        try:
            years_active_wrap = raw_data.pop('years_active')
            years_active = years_active_wrap.pop()
        except IndexError, KeyError:
            pass
        else:
            start = years_active.get('start', "Unknown")
            end = years_active.get('end', "Present")

            data['years_active'] = "(%s - %s)" %(start, end)

        # Image urls.
        try:
            image_wrap = raw_data.pop('images')
            image = image_wrap.pop()
            data['image'] = image.pop('url')
        except (IndexError, KeyError):
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
            buckets=self.BUCKETS)
        self.payload['artist'] = artist
        self.payload['results'] = EchoNestService._RESULT_MAX_LEN
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
            buckets=self.BUCKETS)
        self.payload['name'] = artist

    def __str__(self):
        return "SimilarArtistsService"


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
    

    def __init__(self, **kwargs):
        super(Playlist, self).__init__(self.TYPE_, self.METHOD, 
            buckets=self.BUCKETS, **kwargs)

    def __str__(self):
        return "Playlist"


class SongPlaylistService(Playlist):

    def __init__(self, artist, song):
        dependencies = [
            SongID(song, artist),
        ]

        li = ['one', 'two', 'three']
        srv = ArtistSongsService(artist)
        self.yo = DepMap(srv, li)

        super(SongPlaylistService, self).__init__(dependencies=dependencies)
        self.payload['type'] = "song-radio"
        self.payload['bucket'] += ['audio_summary']

    def __str__(self):
        return "SongPlaylistService"

    def combine_dependency(self, intermediate):
        try:
            first_result = intermediate.pop()
            self.payload['song_id'] = first_result.pop('id')
        except (IndexError, KeyError):
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
            buckets=self.BUCKETS)
        self.dependencies = [SongID(song, artist)]


    def __str__(self):
        return "SongProfileService"

    def combine_dependency(self, intermediate):
        try:
            first_result = intermediate.pop()
            self.payload['song_id'] = first_result.pop('id')
        except (IndexError, KeyError):
            raise EmptyResponseError()

    def process(self, raw_data):
        try:
            first_result = raw_data.pop()
        except IndexError:
            raise EmptyResponseError()
        else:
            data = {}

            # Echo Nest audio analysis.
            try:
                audio = first_result.pop('audio_summary')
            except KeyError:
                pass
            else:
                data['tempo'] = "%s bpm" %(audio.get('tempo'))
                data['danceability'] = to_percent(audio.get('danceability'))
                data['liveness'] = to_percent(audio.get('liveness'))

                # Song duration.
                try:
                    duration = audio.pop('duration')
                    data['duration'] = convert_seconds(duration)
                except KeyError:
                    pass

            # General data.
            data['song_hotttnesss'] = first_result.get('song_hotttnesss')
            data['song_hotttnesss_rank'] = first_result.get('song_hotttnesss_rank')

            return data


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
            buckets=self.BUCKETS)
        self.payload['results'] = EchoNestService._PERSIST


    def __str__(self):
        return "TopArtistsService"




# TODO: remove index error, move try to caller for None str
def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    try:
        s =  percent.pop() + " %"
    except IndexError:
        s =  ''

    return s




# Used to display (M:S) duration on song profile.
def convert_seconds(duration):
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    # time = str(duration)
    # try:
    #     minutes = time.split('.').pop() # this is wrong

    # if len(minutes) > 1:
    #     m = int(minutes) / 60
    #     s = round(duration - (m * 60))
    #     seconds = str(s).split('.')[0]

    #     if len(seconds) < 2:
    #         seconds = seconds + "0"

    #     return "(%s:%s)" %(m, seconds)
    # else:
    #     return "(:%s)" %(minutes[0])

    return ''





