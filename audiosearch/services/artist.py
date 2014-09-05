from __future__ import absolute_import

from audiosearch.services.base import EchoNestService


_N_GENRE_TAGS = 5


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


    def __init__(self, artist):
        payload = dict(name=artist, bucket=ArtistProfile.BUCKETS)
        super(ArtistProfile, self).__init__(self.TYPE_, self.METHOD, 
            payload)

    def __str__(self):
        return "artist profile service"

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


class SimilarArtists(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'similar'
    BUCKETS = [
        'images',
        'terms',
        'songs',
    ]
    ECHO_NEST_KEY = 'artists'


    def __init__(self, artist):
        payload = dict(name=artist, bucket=SimilarArtists.BUCKETS)
        super(ArtistProfile, self).__init__(self.TYPE_, self.METHOD, 
            payload)

    def __str__(self):
        return "SimilarArtists"


class ArtistSongs(EchoNestService):
    TYPE_ = 'playlist'
    METHOD = 'static'
    BUCKETS = [
        'audio_summary',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist):
        payload = {
            'artist': artist,
            'results': EchoNestService._RESULT_MAX_LEN,
            'sort': "song_hotttnesss-desc",
        }
        super(ArtistSongs, self).__init__(self.TYPE_, self.METHOD, payload)

    def __str__(self):
        return "ArtistSongs"
