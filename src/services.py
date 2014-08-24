from __future__ import absolute_import

import audiosearch.constants as constants



class EchoNestServiceFailure(Exception):
    pass

class EmptyServiceResponse(Exception):
    pass




class EchoNestService(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"


    def __init__(self, type_, method, buckets=None):
        self.dependency = None
        self.payload = {
            'api_key': constants.API_KEY,
            'bucket': buckets,
            'format': "json",
        }
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
        super(ArtistProfileService, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.payload['name'] = artist


    def __str__(self):
        return "ArtistProfileService"


    def trim(self, data):
        print self.url
        result = {}

        location_dict = data.get('artist_location')
        if location_dict:
            result['location'] = location_dict.get('location')

        genres = data.get('genres')
        if genres:
            genres = genres[:constants.GENRE_COUNT]
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


class ArtistSongsService(EchoNestService):
    TYPE_ = 'playlist'
    METHOD = 'static'
    BUCKETS = [
        'audio_summary',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist_name):
        super(ArtistSongsService, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.payload['artist'] = artist_name
        self.payload['results'] = constants.RESULTS
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


    def __init__(self, artist_name):
        super(SimilarArtistsService, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.payload['name'] = artist_name
        self.payload['results'] = constants.RESULTS


    def __str__(self):
        return "SimilarArtistsService"


class SearchArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'suggest'
    ECHO_NEST_KEY = 'artists'


    def __init__(self, artist_name):
        super(SearchArtistsService, self).__init__(self.TYPE_, self.METHOD)
        self.payload['name'] = artist_name
        self.payload['results'] = constants.RESULTS


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


    def __init__(self, song_title, artist_name=None):
        super(SearchSongsService, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.payload['title'] = song_title
        self.payload['artist'] = artist_name
        self.payload['results'] = constants.RESULTS
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


    def __str__(self):
        return "SearchSongsService"


# Used to acquire a song's Echo Nest id.
class SongID(SearchSongsService):

    def __init__(self, artist_name, song_title):
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
    

    def __init__(self):
        super(Playlist, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.payload['results'] = constants.RESULTS


    def __str__(self):
        return "Playlist"


class SongPlaylistService(Playlist):
    def __init__(self, artist_name, song_title):
        super(SongPlaylistService, self).__init__()
        self.payload['type'] = "song-radio"
        self.dependency = SongID(song_title, artist_name)


    def __str__(self):
        return "SongPlaylistService"


    # Song playlists require an Echo Nest id to be used as a seed.
    def build(self, intermediate):
        try:
            self.payload['song_id'] = intermediate[0].get('id')

            if not self.payload['song_id']:
                raise EmptyServiceResponse()

        except IndexError:
            raise EmptyServiceResponse()


class ArtistPlaylistService(Playlist):
    def __init__(self, artist_name):
        super(ArtistPlaylistService, self).__init__()
        self.payload['artist'] = artist_name
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


    def __init__(self, artist_name, song_title):
        super(SongProfileService, self).__init__(self.TYPE_, self.METHOD, self.BUCKETS)
        self.dependency = SongID(artist_name, song_title)


    def __str__(self):
        return "SongProfileService"


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
        self.payload['results'] = constants.RESULTS


    def __str__(self):
        return "TopArtistsService"




# TODO: remove index error, move try to caller for None str
def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    try:
        s =  percent[0] + " %"
    except IndexError:
        s =  ''

    return s




# Used to display (M:S) duration on song profile.
def convert_seconds(t):
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






