from __future__ import absolute_import

from audiosearch.models.resource import base


class ArtistProfile(base.BaseResource):

    def __init__(self, name):
        super(ArtistProfile, self).__init__('artist', 'profile', name)
