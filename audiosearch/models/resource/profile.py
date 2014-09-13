from __future__ import absolute_import

from audiosearch.models.resource import base


class ArtistProfile(base.BaseResource):
    _fields = ['artist']
    group = 'artist'
    category = 'profile'


class SongProfile(base.BaseResource):
    _fields = ['artist', 'song']
    group = 'song'
    category = 'profile'
