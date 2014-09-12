from __future__ import absolute_import

from audiosearch.models.resource import base


class TopArtists(base.BaseResource):
    category = 'top'
    content = 'artists'

