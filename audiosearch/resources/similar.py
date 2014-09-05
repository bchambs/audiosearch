from __future__ import absolute_import

from audiosearch.resources.base import BaseResource
from audiosearch.services import SimilarArtists


class Similar(BaseResource):
    _id_tail = 'similar'


    def __init__(self, **kwargs):
        try:
            artist = kwargs.pop('artist')
        except KeyError:
            raise ValueError

        name = artist
        self._id_head = 'artist'
        self._build_service(SimilarArtistsService, artist)

        super(Similar, self).__init__(self._id_head, Similar._id_tail, name)

