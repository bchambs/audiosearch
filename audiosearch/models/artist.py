from __future__ import absolute_import

from audiosearch.models import base
from audiosearch.core import trim

 
ARTIST_GROUP = 'artist'


class Profile(base.EchoNestResource):
    _fields = ['artist']
    bucket = [
        'artist_location',
        'biographies',
        'genre',
        'hotttnesss',
        'images',
        'years_active',
    ]
    description = 'Profile'
    group = ARTIST_GROUP
    method = 'profile'
    response_key = 'artist'
    template = 'artist-home-profile.html'

    @property
    def alias(self):
        return getattr(self, 'artist')

    def get_service_params(self):
        return {
            'bucket': Profile.bucket,
            'name': getattr(self, 'artist'),
        }

    @staticmethod
    def clean(echodata):
        BIO_SOURCE = 'wikipedia'
        IMAGE_COUNT = 5
        neat = {}

        # Artist location (city, region, country)
        location_dict  = echodata.get('artist_location')
        city = location_dict.get('city')
        region = location_dict.get('region')
        country = location_dict.get('country')

        # Biography (first paragraph as summary and full text)
        biography_dicts = echodata.get('biographies')
        for bio in biography_dicts:
            site = bio.get('site')

            # Wikipidea or nothing
            if site == BIO_SOURCE:
                bio_full = bio.get('text')
                paragraphs = bio_full.splitlines() if bio_full else None
                bio_summary = paragraphs[0] if paragraphs else None
                break
        else:
            bio_summary = bio_full = 'Unavailable'

        # Genres (list of strings)
        genre_dicts = echodata.get('genres')
        genres = trim.genres(genre_dicts)

        # Rank (##.###)
        hotttnesss = echodata.get('hotttnesss')
        rank = trim.rank(hotttnesss)

        # Images (list of urls)
        image_dicts = echodata.get('images')
        images = trim.images(image_dicts, IMAGE_COUNT)

        # Years active (start - end), response is a list of dicts (usually 1)
        active_dict = echodata.get('years_active')
        try:
            first_active = active_dict[0]
        except IndexError:
            first_active = {}
        start = first_active.get('start', 'Unknown')
        end = first_active.get('end', 'present')

        neat = {
            'city': city,
            'region': region,
            'country': country,
            'bio_summary': bio_summary,
            'bio_full': bio_full,
            'genres': genres,
            'rank': rank,
            'images': images,
            'active_start': start,
            'active_end': end,
        }

        return neat


class Top_Hottt(base.EchoNestResource):
    _fields = []
    bucket = [
        'genre',
        'hotttnesss',
        'images',
        'songs',
    ]
    description = 'Popular Music'
    group = ARTIST_GROUP
    method = 'top_hottt'
    response_key = 'artists'
    template = 'music-home-content.html'

    @property
    def alias(self):
        return '$'

    @staticmethod
    def get_service_params():
        return {
            'bucket': Top_Hottt.bucket,
            'results': 100,
        }

    @staticmethod
    def clean(echodata):
        GENRES_COUNT = 3
        SONGS_COUNT = 3
        neat = []

        for artist in echodata:
            # Require artist name
            try:
                name = artist.pop('name')
            except KeyError:
                continue

            # Genres (list of strings)
            genre_dicts = artist.get('genres')
            genres = trim.genres(genre_dicts, GENRES_COUNT)

            # Rank (##.###)
            hotttnesss = artist.get('hotttnesss')
            rank = trim.rank(hotttnesss)

            # Display image (url)
            image_dicts = artist.get('images')
            images = trim.images(image_dicts, 1)
            try:
                image_url = images[0]
            except IndexError:
                image_url = None

            # Songs (title and echonest id?)
            song_dicts = artist.get('songs')
            songs = trim.songs(song_dicts, SONGS_COUNT)

            infodict = {
                'name': name,
                'genres': genres,
                'rank': rank,
                'image': image_url,
                'songs': songs,
            }
            neat.append(infodict)

        return neat
