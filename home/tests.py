from django.test import TestCase
from models import ENCall
import urllib
from collections import OrderedDict

# various unit tests
# python manage.py test
class ENCallTestCase(TestCase):

    def setUp(self):
        # constructor setup
        self.arty = ENCall(method='profile', call_type='artist')
        self.song = ENCall(method='profile', call_type='song')
        self.search = ENCall(method='search', call_type='artist')

        # build setup
        self.EN_id = 'ARH6W4X1187B99274F'
        self.standard = [
            'biographies',
            'terms',
            'hotttnesss',
            'images',
            'songs'
        ]


    def test_constructor(self):
        # artist, profile
        self.assertEqual(self.arty.path, "http://developer.echonest.com/api/v4/artist/profile")

        # song, profile
        self.assertEqual(self.song.path, "http://developer.echonest.com/api/v4/song/profile") 

        # artist, search
        self.assertEqual(self.search.path, "http://developer.echonest.com/api/v4/artist/search")


    def test_build(self):
        # artist, standard build
        self.assertEqual(self.arty.build(self.EN_id, self.standard), 'http://developer.echonest.com/api/v4/artist/profile?api_key=QZQG43T7640VIF4FN&format=json&id=ARH6W4X1187B99274F&bucket=biographies&bucket=terms&bucket=hotttnesss&bucket=images&bucket=songs')

        # song, standard build
        self.assertEqual(self.song.build(self.EN_id, self.standard), 'http://developer.echonest.com/api/v4/song/profile?api_key=QZQG43T7640VIF4FN&format=json&id=ARH6W4X1187B99274F&bucket=biographies&bucket=terms&bucket=hotttnesss&bucket=images&bucket=songs')

    def test_consume(self):

