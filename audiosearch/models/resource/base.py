from __future__ import absolute_import

from audiosearch.handlers import get_echo_data

_ARTIST_SONG_SEP = ' BY '
_ID_SEP = ' '
_KEY_SEP = '::'


class BaseResource(object):
    _fields = []    # Map for *args location to attribute in subclass.


    def __init__(self, *args, **kwargs):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        
        # Set all of the positional arguments
        for name, value in zip(self._fields, args):
            setattr(self, name, value)
        
        # Set the remaining keyword arguments
        for name in self._fields[len(args):]:
            setattr(self, name, kwargs.pop(name))
        
        # Check for any remaining unknown arguments
        if kwargs:
            raise TypeError('Invalid argument(s): {}'.format(','.join(kwargs)))

        if self.category == 'artist':
            name = self.artist
        elif self.category == 'song':
            name = _ARTIST_SONG_SEP.join([self.song, self.artist])
        elif self.category == 'top':
            name = '$'
        else:
            raise TypeError('Unexpected category')

        self._rid = _ID_SEP.join([self.category, self.content])
        self._key = _KEY_SEP.join([self._rid, name])
        self._name = name


    def __cmp__(self, other):
        return (ord(self.key) < ord(other.key))


    def __getitem__(self, key):
        return getattr(self, key)


    def __repr__(self):
        return "%s for %s" % (self.rid, self.name)


    @property
    def rid(self):
        return self._rid


    @property
    def key(self):
        return self._key


    def get(self):
        params = dict([(field, getattr(self, field)) for field in self._fields])
        get_echo_data(self.key, self.category, self.content, params)
