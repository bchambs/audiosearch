from __future__ import absolute_import

from audiosearch.models.resource import base


class ArtistProfile(base.BaseResource):
    _fields = ['artist']
    _storage_type = dict
    group = 'artist'
    category = 'profile'


class SongProfile(base.BaseResource):
    _fields = ['artist', 'song']
    _storage_type = dict
    group = 'song'
    category = 'profile'
