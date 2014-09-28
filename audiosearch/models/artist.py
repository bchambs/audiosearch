from __future__ import absolute_import

from audiosearch.models import base


MGROUP = 'artist'


class Profile(base.BaseResource):
    _params = ['bucket', 'name']
    bucket = [
        'artist_location',
        'genre',
        'years_active',
    ]
    description = 'Profile'
    method = 'profile'
    response_key = 'artist'


    def __init__(self, name):
        super(Profile, self).__init__(MGROUP, Profile.method, name)


class TopHottt(base.BaseResource):
    _params = ['results']
    description = 'Popular Music'
    method = 'top_hottt'
    response_key = 'artists'
    results = 100

    def __init__(self):
        name = '$'
        super(TopHottt, self).__init__(MGROUP, TopHottt.method, name)

