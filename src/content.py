from __future__ import absolute_import

import src.services as services


_SEPARATOR = "==="


def build_key(prefix , content_id, *pieces):
    return _SEPARATOR.join([prefix] + map(str,pieces) + [content_id])

class Resource(object):
    TTL = 3000

class ArtistResource(Resource):
    PREFIX = "artist"

class ArtistProfile(ArtistResource):
    CONTENT_ID = "artist_profile"


    def __init__(self, artist):
        self.artist = artist
        self.content_id = ArtistProfile.CONTENT_ID
        self.key = build_key(ArtistResource.PREFIX, ArtistProfile.CONTENT_ID, 
            self.artist)


    def __str__(self):
        return "ArtistProfile"


    def build(self):
        return services.ArtistProfileService(self.artist)


class ArtistSongs(ArtistResource):
    CONTENT_ID = "artist_songs"


    def __init__(self, artist):
        self.artist = artist
        self.content_id = ArtistSongs.CONTENT_ID
        self.key = build_key(ArtistResource.PREFIX, ArtistSongs.CONTENT_ID, 
            self.artist)


    def __str__(self):
        return "ArtistSongs"


    def build(self):
        return services.ArtistSongsService(self.artist)



class TopResource(object):
    PREFIX = "top"
    TTL = 0

class TopArtists(TopResource):
    CONTENT_ID = "top_artists"


    def __init__(self):
        self.content_id = TopArtists.CONTENT_ID
        self.key = build_key(TopResource.PREFIX, TopArtists.CONTENT_ID)


    def __str__(self):
        return "TopArtists"


    def build(self):
        return services.TopArtistsService()
