from __future__ import absolute_import

from audiosearch.models import base
from audiosearch.core import trim

 
GROUP = 'artist'


class ArtistMixin(object):
    _fields = ['artist']
    group = 'artist'

    @property
    def alias(self):
        return getattr(self, 'artist', base.DEFAULT_ALIAS)


class Profile(base.EchoNestResource, ArtistMixin):
    bucket = [
        'artist_location',
        'biographies',
        'genre',
        'hotttnesss',
        'images',
        'years_active',
    ]
    description = 'Profile'
    method = 'profile'
    response_key = 'artist'
    template = 'artist-home-profile.html'

    def get_service_params(self):
        return {
            'bucket': Profile.bucket,
            'name': self.artist,
        }

    def clean(self, echodata):
        BIO_SOURCE = 'wikipedia'
        neat = {}

        # Artist location (city, region, country)
        try:
            location_dict = echodata.pop('artist_location')
        except KeyError:
            city = region = country = None
        else:
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
        genres = trim.genres(genre_dicts) if genre_dicts else []

        # Rank (##.###)
        hotttnesss = echodata.get('hotttnesss')
        rank = trim.rank(hotttnesss) if hotttnesss else None

        # Images (list of urls)
        image_dicts = echodata.get('images')
        images = trim.images(image_dicts) if image_dicts else []

        # Years active (start - end)
        try:
            years_active_dict = echodata.pop('years_active')[0]
        except (IndexError, KeyError):
            start, end = None
        else:
            start = years_active_dict.get('start', 'Unknown')
            end = years_active_dict.get('end', 'present')

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


class Top_Hottt(base.EchoNestResource, ArtistMixin):
    _fields = []
    bucket = [
        'genre',
        'hotttnesss',
        'images',
        'songs',
    ]
    description = 'Popular Music'
    method = 'top_hottt'
    response_key = 'artists'
    template = 'music-home-content.html'

    def get_service_params(self):
        return {
            'bucket': Top_Hottt.bucket,
            'results': 100,
        }

    def clean(self, echodata):
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
            genres = trim.genres(genre_dicts, GENRES_COUNT) if genre_dicts else []

            # Rank (##.###)
            hotttnesss = artist.get('hotttnesss')
            rank = trim.rank(hotttnesss) if hotttnesss else None

            # Display image (url)
            image_dicts = artist.get('images', [])
            images = trim.images(image_dicts, 1) if image_dicts else None
            image_url = images[0] if len(images) else None

            # Songs (title and echonest id?)
            song_dicts = artist.get('songs', [])
            seen = set('default')
            songs = []
            for song in song_dicts:
                title = song.get('title', 'default')
                
                # Do not display duplicate songs with different echo ids
                if title not in seen:
                    seen.add(title)
                    songs.append(song)
                if len(songs) >= SONGS_COUNT:
                    break

            infodict = {
                'name': name,
                'genres': genres,
                'rank': rank,
                'image': image_url,
                'songs': songs,
            }
            neat.append(infodict)

        return neat
