from __future__ import absolute_import

from audiosearch.models import base


GROUP = 'artist'


class ArtistMixin(object):
    group = 'artist'

    def get_alias(self):
        return getattr(self, 'artist', '$')


class Profile(base.EchoNestResource, ArtistMixin):
    _fields = ['artist']
    bucket = [
        'artist_location',
        'genre',
        'years_active',
    ]
    description = 'Profile'
    method = 'profile'
    response_key = 'artist'

    def get_params(self):
        return {
            'bucket': Profile.bucket,
            'name': self.artist,
        }


class Top_Hottt(base.EchoNestResource, ArtistMixin):
    _fields = []
    description = 'Popular Music'
    method = 'top_hottt'
    response_key = 'artists'

    def get_params(self):
        return {
            'results': 100,
        }
