from __future__ import absolute_import

from audiosearch.models.resource import base


class ArtistProfile(base.BaseResource):
    _fields = ['artist']
    category = 'artist'
    content = 'profile'
    _ttl = 0
