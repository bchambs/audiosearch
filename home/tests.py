from django.test import SimpleTestCase
from models import ENCall, ExceededCallLimit
import requests
from util import debug, debug_l, debug_title, debug_subtitle, get_test_json


# various unit tests
# python manage.py test
class ENCallTestCase(SimpleTestCase):

    def setUp(self):
        debug_title('begin constructor')

        # constructor setup
        self.arty = ENCall(method='profile', call_type='artist')
        self.song = ENCall(method='profile', call_type='song')
        self.search = ENCall(method='search', call_type='artist')

        self.artist_id = 'ARH6W4X1187B99274F'
        self.song_id = 'SOCZMFK12AC468668F'

        # artist param setup
        self.artist_name = 'radiohead'
        self.artist_bucket = [
            'biographies',
            'terms',
            'hotttnesss',
            'images',
            'songs'
        ]
        self.artist_dict = {
            "api_key": "QZQG43T7640VIF4FN",
            "format": "json",
            'bucket': self.artist_bucket,
            'id': self.artist_id
        }

        # song param setup
        self.song_bucket = [
            'song_hotttnesss'
        ]
        self.song_dict = {
            "api_key": "QZQG43T7640VIF4FN",
            "format": "json",
            'bucket': self.song_bucket,
            'id': self.song_id
        }

        # search artist param setup
        self.search_dict = {
            "api_key": "QZQG43T7640VIF4FN",
            "format": "json",
            'bucket': self.artist_bucket,
            'name': self.artist_name
        }
        
        # artist, profile
        self.assertEqual(self.arty.path, "http://developer.echonest.com/api/v4/artist/profile")

        # song, profile
        self.assertEqual(self.song.path, "http://developer.echonest.com/api/v4/song/profile") 

        # artist, search
        self.assertEqual(self.search.path, "http://developer.echonest.com/api/v4/artist/search")


    # I am unable to have django run tests in order.  build and consume must be combined.
    def test_build_and_consume(self):
        debug_title('begin build')
        
        # artist, standard build
        # compare test and control param dicts (query string)
        empty = {}
        self.arty.build(self.artist_id, empty, self.artist_bucket)
        self.assertEqual(len(self.artist_dict), len(self.arty.data))

        for k, v in self.arty.data.iteritems():
            self.assertTrue(k in self.artist_dict)
            self.assertEqual(self.artist_dict[k], v)

        # song, standard build
        empty = {}
        self.song.build(self.song_id, empty, self.song_bucket)
        self.assertEqual(len(self.song_dict), len(self.song.data))

        for k, v in self.song.data.iteritems():
            self.assertTrue(k in self.song_dict)
            self.assertEqual(self.song_dict[k], v)

        # search, standard build
        empty = {}
        self.search.build(self.artist_name, empty, self.artist_bucket)
        self.assertEqual(len(self.search_dict), len(self.search.data))

        debug(self.search.data.keys())
        debug(self.search_dict.keys())

        for k, v in self.search.data.iteritems():
            self.assertTrue(k in self.search_dict)
            self.assertEqual(self.search_dict[k], v)

        # this is a mess, I am done with this until I have time to look into django's testing.
        # test consume
        # debug_title('begin consume')

        # artist_profile_url = 'http://developer.echonest.com/api/v4/artist/profile?api_key=QZQG43T7640VIF4FN&bucket=biographies&bucket=terms&bucket=hotttnesss&bucket=images&bucket=songs&id=ARH6W4X1187B99274F&format=json'
        # song_profile_url = 'http://developer.echonest.com/api/v4/song/profile?api_key=QZQG43T7640VIF4FN&bucket=song_hotttnesss&id=SOCZMFK12AC468668F&format=json'
        # artist_search_url = 'http://developer.echonest.com/api/v4/artist/search?api_key=QZQG43T7640VIF4FN&bucket=biographies&bucket=terms&bucket=hotttnesss&bucket=images&bucket=songs&name=radiohead&format=json'

        # # artist profile
        # # compare test and control json
        # debug_subtitle('consume artist')
        # artist_profile_json = self.arty.consume()

        # control_1 = get_test_json(artist_profile_url,'artist')
        # for k, v in artist_profile_json.keys():
        #     self.assertTrue(k in control_1.keys())
        #     self.assertEqual(control_1[k], v)

        # # song profile
        # debug_subtitle('consume song')
        # song_profile_json = self.song.consume()

        # # artist search
        # debug_subtitle('consume search')
        # artist_search_json = self.search.consume()

