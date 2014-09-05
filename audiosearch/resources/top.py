from __future__ import absolute_import

from audiosearch.resources.base import BaseResource
from audiosearch.services.top import TopArtistsService

# Type matching for init.
_ARTISTS = 'artists'


class Top(BaseResource):
    _id_head = 'top'


    def __init__(self, type_):
        name = 'None'

        if type_ == _ARTISTS:
            self._id_tail = 'artists'
            self._build_service(TopArtistsService)
        else:
            raise ValueError

        super(Top, self).__init__(self._id_head, Top._id_tail, name)

