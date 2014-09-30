from __future__ import absolute_import

from audiosearch.models import base


GROUP = 'artist'


class Profile(base.EchoNestResource):
    # _params = ['bucket', 'name']
    _fields = ['artist']
    bucket = [
        'artist_location',
        'genre',
        'years_active',
    ]
    description = 'Profile'
    method = 'profile'
    response_key = 'artist'

    def __init__(self, name):
        super(Profile, self).__init__(GROUP, Profile.method, name)
        self.name = name
        self._params = dict(bucket=Profile.bucket, name=name)


class Top_Hottt(base.EchoNestResource):
    # _params = ['results']
    _fields = {}
    description = 'Popular Music'
    method = 'top_hottt'

    response_key = 'artists'
    results = 100

    def __init__(self):
        super(Top_Hottt, self).__init__(GROUP, Top_Hottt.method)
