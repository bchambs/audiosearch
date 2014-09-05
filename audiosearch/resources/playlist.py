from __future__ import absolute_import

from audiosearch.resources.base import BaseResource, _ARTIST_SONG_SEP
from audiosearch.services.playlist import (SongPlaylistService, 
    ArtistPlaylistService)


class Playlist(BaseResource):
    _id_tail = 'playlist'


    def __init__(self, **kwargs):
        try:
            artist = kwargs.pop('artist')
        except KeyError:
            raise ValueError

        try:
            song = kwargs.pop('song')
            name = _ARTIST_SONG_SEP.join[song, artist]
            self._id_head = 'song'
            self._build_service(SongPlaylistService, artist, song)

        except KeyError:
            name = artist
            self._id_head = 'artist'
            self._build_service(ArtistPlaylistService, artist)

        super(Playlist, self).__init__(self._id_head, Playlist._id_tail, name)

