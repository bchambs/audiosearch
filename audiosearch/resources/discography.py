from __future__ import absolute_import

from audiosearch.resources.base import BaseResource
from audiosearch.services import ArtistSongs


class Discography(BaseResource):
    _id_tail = 'discography'


    def __init__(self, **kwargs):
        try:
            artist = kwargs.pop('artist')
        except KeyError:
            raise ValueError

        name = artist
        self._id_head = 'artist'
        self._build_service(ArtistSongsService, artist)

        super(Discography, self).__init__(self._id_head, Discography._id_tail, name)
