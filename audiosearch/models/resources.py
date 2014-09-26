from __future__ import absolute_import


EMPTY_KEY_PIECE = '$'
ID_SEP = '_'
KEY_SEP = '::'
SONG_SEP = ' BY '


def make_id(head, tail):
    """A resource ID signifies which method from which data group
    a resource represents.  IDs are used as cache key prefixes and 
    resource-to-service mapping.
    """

    return ID_SEP.join([head, tail])


def make_key(id_, name):
    """Create the associated cache key for the resource defined by `id_` and
    `name`.
    """

    return KEY_SEP.join([id_, name])


class BaseResource(object):
    """Core music data class mapping page content to Echo Nest keywords and
    defining parameters.  Used to build cache key from page requests.  Used as
    the specification for building and consuming services with the Echo Nest
    API.
    """

    # Positional args mapping for init.  Override in place of defining init.
    _fields = []

    description = None
    echo_type = list   # TODO: have something else handle this
    group = None
    key = None
    method = None
    name = None
    rid = None  # Resource id
    spec = None


    def __init__(self, *args):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))

        # Set field attributes
        for field, value in zip(self._fields, args):
            setattr(self, field, value)

        params = self.__dict__ or None

        if self.group == 'artist':
            name = self.artist
        elif self.group == 'song':
            name = SONG_SEP.join([self.song, self.artist])
        else:
            name = EMPTY_KEY_PIECE

        self.rid = make_id(self.group, self.method)
        self.key = make_key(self.rid, name)
        self.name = name
        self.params = params


    def __repr__(self):
        return "%s for %s" % (self.rid, self.name)


class TopArtists(BaseResource):
    group = 'top'
    method = 'artists'
    description = 'Popular artists'


class Artist(BaseResource):
    group = 'artist'


    def __init__(self, name):
        self.group = Artist.group
        self.name = name


    @classmethod
    def top(cls):
        self.group = Artist.group

# class ArtistProfile(BaseResource):
#     _fields = ['artist']
#     _storage_type = dict
#     group = 'artist'
#     method = 'profile'


# class SongProfile(BaseResource):
#     _fields = ['artist', 'song']
#     _storage_type = dict
#     group = 'song'
#     method = 'profile'


# class Discography(BaseResource):
#     _fields = ['artist']
#     group = 'artist'
#     method = 'discography'

