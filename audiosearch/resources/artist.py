from __future__ import absolute_import

from audiosearch.resources.base import Resource
from audiosearch.services import services


class Artist(Resource):
    res_type = 'artist'

    def __init__(self, content_type, name):
        self.name = name
        super(Artist, self).__init__(Artist.res_type, 
            content_type, name)


class ArtistProfile(Artist):
    con_type = 'profile'

    def __init__(self, name):
        super(ArtistProfile, self).__init__(ArtistProfile.con_type, name)

    def __str__(self):
        return "%s profile" %(self.name)

    def _build_service(self):
        return services.ArtistProfileService(self.name)



