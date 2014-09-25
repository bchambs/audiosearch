from __future__ import absolute_import

from audiosearch.models.service.base import EchoNestService


_N_GENRE_TAGS = 5


class ArtistProfile(EchoNestService):
    _type = 'artist'
    _method = 'profile'
    _buckets = [
        'artist_location',
        'biographies',
        'images',
        'hotttnesss',
        'genre',
        'years_active',
    ]
    requires_processing = True
    response_data_key = 'artist'


    def __init__(self, artist):
        payload = dict(name=artist, bucket=ArtistProfile._buckets)
        super(ArtistProfile, self).__init__(ArtistProfile._type, 
                                            ArtistProfile._method, **payload)
            

    # redo
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


class ArtistSongs(EchoNestService):
    _type = 'playlist'
    _method = 'static'
    _buckets = [
        'audio_summary',
    ]
    response_data_key = 'songs'


    def __init__(self, artist):
        payload = {
            'artist': artist,
            'results': EchoNestService.max_results,
            'sort': "song_hotttnesss-desc",
        }
        super(ArtistSongs, self).__init__(ArtistSongs._type, ArtistSongs._method,
                                            **payload)


class SearchArtists(EchoNestService):
    _type = 'artist'
    _method = 'suggest'
    response_data_key = 'artists'


    def __init__(self, artist):
        payload = dict(name=artist)
        super(SearchArtists, self).__init__(SearchArtists._type, 
                                            SearchArtists._method, **payload)


class SimilarArtists(EchoNestService):
    _type = 'artist'
    _method = 'similar'
    _buckets = [
        'images',
        'terms',
        'songs',
    ]
    response_data_key = 'artists'


    def __init__(self, artist):
        payload = dict(name=artist, bucket=SimilarArtists._buckets)
        super(ArtistProfile, self).__init__(SimilarArtists._type, 
                                            SimilarArtists._method, **payload)


# TODO: create scheduled service to update this.
class TopArtists(EchoNestService):
    _type = 'artist'
    _method = 'top_hottt'
    _buckets = [
        'hotttnesss_rank',
    ]
    response_data_key = 'artists'


    def __init__(self):
        payload = {
            'results': EchoNestService.max_results,
            'bucket': TopArtists._buckets,
        }
        super(TopArtists, self).__init__(TopArtists._type, TopArtists._method, 
                                        **payload)

