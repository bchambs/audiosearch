from __future__ import absolute_import

from audiosearch.models.resource.base import BaseResource


class TopArtists(BaseResource):
    group = 'top'
    category = 'artists'
    description = 'Popular artists'

