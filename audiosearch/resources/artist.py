from __future__ import absolute_import

from audiosearch.resources.base import BaseResource
from audiosearch.services.artist import (ArtistProfileService, ArtistSongsService)


class Artist(BaseResource):
    resource_id = 'artist'

    def __init__(self, content_type, name):
        self._name = name
        super(Artist, self).__init__(Artist.resource_id, 
            content_type, name)


class ArtistProfile(Artist):
    content_id = 'profile'

    def __init__(self, name):
        super(ArtistProfile, self).__init__(ArtistProfile.content_id, name)

    def __str__(self):
        return "%s profile" %(self.name)

    def build_service(self):
        return ArtistProfileService(self.name)


class ArtistSongs(Artist):
    content_id = 'songs'

    def __init__(self, name):
        super(ArtistSongs, self).__init__(ArtistSongs.content_id, name)

    def __str__(self):
        return "%s profile" %(self._name)

    def build_service(self):
        return ArtistSongsService(self.name)
