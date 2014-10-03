from __future__ import absolute_import

from audiosearch.models import base


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
        'genre',
        'years_active',
    ]
    description = 'Profile'
    method = 'profile'
    response_key = 'artist'

    def get_service_params(self):
        return {
            'bucket': Profile.bucket,
            'name': self.artist,
        }


class Top_Hottt(base.EchoNestResource, ArtistMixin):
    _fields = []
    bucket = [
        'genre',
        'images',
        'songs',
    ]
    description = 'Popular Music'
    method = 'top_hottt'
    response_key = 'artists'

    def get_service_params(self):
        return {
            'bucket': Top_Hottt.bucket,
            'results': 100,
        }

    def trim(self, echodata):
        BAD_IMAGES = set('myspace')
        GENRES_COUNT = 3
        SONGS_COUNT = 2
        trimmed = []

        for artist in echodata:
            # Require artist name
            try:
                name = artist.pop('name')
            except KeyError:
                continue

            # Genres
            genre_dicts = artist.get('genres', [])
            genres = []
            for genre in genre_dicts[:GENRES_COUNT]:
                genre_text = genre.get('name')
                if genre_text:
                    genres.append(genre_text)

            # Songs
            song_dicts = artist.get('songs', [])
            # Do not display duplicate songs with different echo ids
            seen = set('default')
            songs = []
            for song in song_dicts:
                title = song.get('title', 'default')
                
                if title not in seen:
                    seen.add(title)
                    songs.append(song)
                if len(songs) > SONGS_COUNT:
                    break

            # Display image
            image_dicts = artist.get('images', [])
            for img in image_dicts:
                attribution = img.get('attribution', 'n/a')

                if attribution not in BAD_IMAGES:
                    image_url = img.get('url')
                    
                    if image_url:
                        break
            else:
                image_url = None

            infodict = {
                'name': name,
                'genres': genres,
                'songs': songs,
                'image': image_url,
            }
            trimmed.append(infodict)

        return trimmed


    def dbg(self, data):
        return data
        debugged = []
        images = data.get('images')

        for image in images:
            d = {}

            d['url'] = image.get('url')
            d['verified'] = image.get('verified')
            d['license'] = image.get('license')
            d['tags'] = image.get('tags')

            debugged.append(d)

        # t = debugged[0]
        # for k, v in t.iteritems():
        #     print k
        #     print type(v)

        # print t['license'].keys()

        return debugged
