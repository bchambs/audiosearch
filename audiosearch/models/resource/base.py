"""
TODO: make resource classes use a 2 layered dict instead similar to service factory
"""
from __future__ import absolute_import

from audiosearch.core import echonest


EMPTY_KEY_PIECE = '$'
ID_SEP = '_'
KEY_SEP = '::'
SONG_SEP = ' BY '


def make_id(head, tail):
    """Key prefix."""
    return ID_SEP.join([head, tail])


def make_key(id_, name):
    return KEY_SEP.join([id_, name])


class BaseResource(object):
    _fields = []
    _echo_type = list    # Profiles overwrite this to dict


    def __init__(self, *args):
        if len(args) > len(self._fields):
            raise TypeError('Expected {} arguments'.format(len(self._fields)))
        
        # Set field attributes
        for field, value in zip(self._fields, args):
            setattr(self, field, value)

        # Determine key-name by resource group
        if self.group == 'artist':
            name = self.artist
        elif self.group == 'song':
            name = SONG_SEP.join([self.song, self.artist])
        else:
            name = EMPTY_KEY_PIECE

        self._resource_id = make_id(self.group, self.category)
        self._key = make_key(self._resource_id, name)
        self._name = name


    def __eq__(self, other):
        return self.key == other.key


    def __cmp__(self, other):
        return (ord(self.key) < ord(other.key))


    def __ne__(self, other):
        return self.key != other.key


    def __repr__(self):
        return "%s for %s" % (self._resource_id, self._name)


    @property
    def echo_type(self):
        return self._echo_type


    @property
    def key(self):
        return self._key


    # @property
    # def name(self):
        # return self._name

    @property
    def resource_id(self):
        return self._resource_id


    # REDO
    def retrieve(self):
        resource_params = dict([
            (field, getattr(self, field)) 
            for field 
            in self._fields])
        echonest.get_resource(self.key, self.group, self.category, 
            resource_params)


    # REDO
    def async_rep(self):
        return self._group, self._category, self._name
