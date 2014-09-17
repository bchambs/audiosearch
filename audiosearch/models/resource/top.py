from __future__ import absolute_import

from audiosearch.models.resource import base


class TopArtists(base.BaseResource):
    group = 'top'
    category = 'artists'
    description = 'Popular artists'

