from __future__ import absolute_import

from audiosearch.resources.base import (BaseResource, wrap_service, 
    _ARTIST_SONG_SEP)
from audiosearch.services.artist import ArtistProfileService
from audiosearch.services.song import SongProfileService


class Profile(BaseResource):
    _id_tail = 'profile'


    def __init__(self, **kwargs):
        try:
            artist = kwargs.pop('artist')
        except KeyError:
            raise ValueError

        try:
            song = kwargs.pop('song')
            name = _ARTIST_SONG_SEP.join[song, artist]
            self._id_head = 'song'
            self._build_service(SongProfileService, artist, song)

        except KeyError:
            name = artist
            self._id_head = 'artist'
            self._build_service = wrap_service(ArtistProfileService, artist)

        super(Profile, self).__init__(self._id_head, Profile._id_tail, name)
