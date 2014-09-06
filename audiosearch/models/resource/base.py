from __future__ import absolute_import

from audiosearch import handlers


_ARTIST_SONG_SEP = ' BY '
_KEY_SEP = '::'


class BaseResource(object):
    _ttl = 3000

    def __init__(self, id_head, id_tail, name):
        self._id = (id_head, id_tail)
        self._key = _KEY_SEP.join([id_head, id_tail, name])

    @property
    def id(self):
        return self._id

    @property
    def key(self):
        return self._key

    @property
    def ttl(self):
        return self._ttl




# class EchoResource(BaseResource):
#     _ttl = _DEFAULT_TTL

#     def __init__(self, echo_type, resource_type, **kwargs):
#         try:
#             if echo_type == 'artist':
#                 artist = kwargs.pop('artist')
#                 name = artist
 
#             else:
#                 raise ValueError()
#         except KeyError:
#             raise ValueError()
#         else:
#             super(EchoResource, self).__init__(echo_type, resource_type, name)

#     @property
#     def miss_handler(self):
#         return handlers.get_echo_data(self._id, self._key, self._ttl) 
                                       

# def _song_by_artist(artist, song):
#     return _ARTIST_SONG_SEP.join([song, artist])

