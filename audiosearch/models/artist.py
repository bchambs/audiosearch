from __future__ import absolute_import

from audiosearch.models import base


MGROUP = 'ARTIST'


class Profile(base.BaseResource):
    bucket = [
        'artist_location',
        'genre',
        'years_active',
    ]
    method = 'PROFILE'
    response_key = 'artist'

    def __init__(self, name):
        super(Profile, self).__init__(MGROUP, Profile.method, name)

    @property
    def params(self):
        return dict(name=self.name)
