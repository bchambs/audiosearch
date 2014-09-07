from __future__ import absolute_import

from audiosearch.models.resource import base


class Discography(base.BaseResource):

    def __init__(self, name):
        super(Discography, self).__init__('artist', 'discography', name)
