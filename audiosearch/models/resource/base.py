from __future__ import absolute_import

from audiosearch import handlers
from audiosearch import DEFAULT_TTL


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
            name = _ARTIST_SONG_SEP.join([self._song, self.artist])
        else:
            raise TypeError('Unexpected category')

        key_id = _ID_SEP.join([self.category, self.content])
        self.key = _KEY_SEP.join([key_id, name])
        self.name = name


    def __cmp__(self, other):
        print ord(self.key)
        print ord(other.key)
        return (ord(self.key) < ord(other.key))


    def __repr__(self):
        return "%s %s for %s" % (self.category, self.content, self.name)


    @property
    def category(self):
        return self.category


    @property
    def content(self):
        return self.content


    @property
    def ttl(self):
        if getattr(self, '_ttl', None) is None:
            self._ttl = DEFAULT_TTL
        return self._ttl


