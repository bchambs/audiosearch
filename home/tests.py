from django.test import TestCase
from models import ENCall
import urllib
from collections import OrderedDict

from pyechonest import config
config.ECHO_NEST_API_KEY="QZQG43T7640VIF4FN"
from pyechonest import artist

# various unit tests
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
        self.assertEqual(self.arty.LEAD, 'http://developer.echonest.com/api/')
        self.assertEqual(self.arty.VERSION, 'v4/')
        self.assertEqual(self.arty.CTYPE, 'artist/')
        self.assertEqual(self.arty.METHOD, 'profile')
        self.assertEqual(self.arty.KEY, 'api_key=QZQG43T7640VIF4FN')
        self.assertEqual(self.arty.FORMAT, '&format=json')

        # song, profile
        self.assertEqual(self.song.LEAD, 'http://developer.echonest.com/api/')
        self.assertEqual(self.song.VERSION, 'v4/')
        self.assertEqual(self.song.CTYPE, 'song/')
        self.assertEqual(self.song.METHOD, 'profile')
        self.assertEqual(self.song.KEY, 'api_key=QZQG43T7640VIF4FN')
        self.assertEqual(self.song.FORMAT, '&format=json')

        # song, search
        self.assertEqual(self.search.LEAD, 'http://developer.echonest.com/api/')
        self.assertEqual(self.search.VERSION, 'v4/')
        self.assertEqual(self.search.CTYPE, 'artist/')
        self.assertEqual(self.search.METHOD, 'search')
        self.assertEqual(self.search.KEY, 'api_key=QZQG43T7640VIF4FN')
        self.assertEqual(self.search.FORMAT, '&format=json')


    def test_build(self):
        # artist, standard build
        self.assertEqual(self.arty.build(self.EN_id, self.standard), 'http://developer.echonest.com/api/v4/artist/profile?api_key=QZQG43T7640VIF4FN&format=json&id=ARH6W4X1187B99274F&bucket=biographies&bucket=terms&bucket=hotttnesss&bucket=images&bucket=songs')


    def e(self):
        d = OrderedDict()
        d['key'] = 'api_key=QZQG43T7640VIF4FN'
        d['format'] = '&format=json'
        d['EN_id'] = '&id=ARH6W4X1187B99274F'
        
        d['bucket'] = 'biographies', 'terms'
        #     'terms',
        #     'hotttnesss',
        #     'images',
        #     'songs'
        # ]

        url =  urllib.urlencode(d)
        print urllib.unquote(url)

    def f(self):
        a = artist.Artist(id='ARH6W4X1187B99274F')
        print a
