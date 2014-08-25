"""
Redis key format:
    resource_type :: *names :: content_type
    resource_type :: none :: content_type


c_type = content type (key suffix)
d_type = data type 
r_type = resource type (key prefix)

"""

from __future__ import absolute_import

from audiosearch.constants import DICT_, LIST_, STR_, STANDARD_TTL
from audiosearch.redis_client import K_SEPARATOR
import src.services as services


# Key prefixes representing the content type of a resource.
ARTIST = "artist"
SEARCH = "search"
SONG = "song"
TOP = "top"
TRENDING = "trending"

# Key suffixes representing the content type. 
ARTISTS = "artists"
PLAYLIST = "playlist"
PROFILE = "profile"
SIMILAR = "similar"
SONGS = "songs"

# Template mappings.
T_SEPARATOR = "_"


class InvalidContentError(Exception):
    """Invalid parameters passed to content constructor."""
        

def build_keys(prefix, suffix, root=None):
    # Redis cache key.
    root = root or ["none"]
    key_parts = [prefix] + root + [suffix]
    key = K_SEPARATOR.join(key_parts)

    # Template content id.
    template_id = "%s%s%s" %(prefix, T_SEPARATOR, suffix)

    return key, template_id


class Profile(object):
    c_type = PROFILE
    d_type = DICT_
    ttl = STANDARD_TTL


    def __init__(self, artist, song=None):
        self.artist = artist

        # Song Profile.
        if song:
            self.r_type = SONG
            self.song = song
            root = [artist, song]

        # Artist Profile.
        else:
            self.r_type = ARTIST
            root = [artist]

        self.title = "%s Profile" %(self.r_type.title())
        self.key, self.template_id = build_keys(self.r_type, self.c_type, root)


    def __str__(self):
        return "%s Profile" %(self.r_type.title())


    # Create service object.  Determined by content type.
    def build_service(self):
        if self.r_type == ARTIST:
            return services.ArtistProfileService(self.artist)
        elif self.r_type == SONG:
            return services.SongProfileService(self.artist, self.song)


class Top100(object):
    c_type = ARTISTS
    d_type = LIST_
    ttl = 0


    # Currently 'artists' is the only valid type.
    # TODO: implement songs and genres(sort top by genre?) top 100.
    def __init__(self, content_type):
        self.r_type = TOP

        if content_type == ARTISTS:
            self.c_type = ARTISTS
        else:
            raise InvalidContentError()

        self.title = "Popular %s" %(self.c_type.title())
        self.key, self.template_id = build_keys(self.r_type, self.c_type)


    def __str__(self):
        return "Top 100 %s" %(self.c_type)


    # Create service object.  Determined by content subtype.
    def build_service(self):
        if self.c_type == ARTISTS:
            return services.TopArtistsService()



