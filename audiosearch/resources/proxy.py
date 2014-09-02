from __future__ import absolute_import

from audiosearch.resources import artist


class Profile(object):

    def __new__(self, **kwargs):
        artist_ = kwargs.pop('artist')
        song_ = kwargs.get('song')

        if song_:
            pass
        else:
            return artist.ArtistProfile(artist_)
