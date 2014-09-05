from __future__ import absolute_import

from audiosearch.resources.base import BaseResource
from audiosearch import services


class Profile(BaseResource):
    _id_tail = 'profile'


    def __init__(self, **kwargs):
        try:
            artist = kwargs.pop('artist')
        except KeyError:
            raise ValueError

        try:
            song = kwargs.pop('song')
            name = BaseResource._song_by_artist(artist, song)
            self._id_head = 'song'
            # self._build_service(SongProfileService, artist, song)

        except KeyError:
            name = artist
            self._id_head = 'artist'
            # self._build_service = wrap_service(ArtistProfileService, artist)

        super(Profile, self).__init__(self._id_head, Profile._id_tail, name)
