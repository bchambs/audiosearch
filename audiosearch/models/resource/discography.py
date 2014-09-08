from __future__ import absolute_import

from audiosearch.models.resource import base


class Discography(base.BaseResource):
    _fields = ['artist']
    category = 'artist'
    content = 'discography'

