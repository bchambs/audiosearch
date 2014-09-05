from __future__ import absolute_import

from django.test import SimpleTestCase

from audiosearch.resources import (discography, playlist, profile, search, 
    similar, top)

_ARTIST = 'bright eyes'
_SONG = 'train under water'


class TestProfile(SimpleTestCase):

    def setUp(self):
        self.artist_profile = profile.Profile(artist=_ARTIST)
        self.song_profile = profile.Profile(artist=_ARTIST, song=_SONG)

