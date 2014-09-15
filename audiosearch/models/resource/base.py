from __future__ import absolute_import

from audiosearch.handlers import get_echo_data
from audiosearch.models import make_id, make_key


_ARTIST_SONG_SEP = ' BY '


class BaseResource(object):
    _fields = []    # Map for *args location to attribute in subclass
    _storage_type = list    # Profiles overwrite this to dict


    def __init__(self, *args):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        
        for field, value in zip(self._fields, args):
            setattr(self, field, value)

        if self.group == 'artist':
            name = self.artist
        elif self.group == 'song':
            name = _ARTIST_SONG_SEP.join([self.song, self.artist])
        else:
            name = '$'

        self._res_id = make_id(self.group, self.category)
        self._key = make_key(self._res_id, name)
        self._name = name


    def __cmp__(self, other):
        return (ord(self.key) < ord(other.key))


    def __getitem__(self, key):
        return getattr(self, key)


    def __repr__(self):
        return "%s for %s" % (self._res_id, self._name)


    @property
    def echo_type(self):
        return self._storage_type


    @property
    def key(self):
        return self._key


    @property
    def name(self):
        return self._name


    @property
    def res_id(self):
        return self._res_id


    def get_resource(self):
        params = dict([(field, getattr(self, field)) for field in self._fields])
        get_echo_data(self.key, self.group, self.category, params)
