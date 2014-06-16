import json
import requests
import urllib

__all__ = ['ENC']

# avoid side effects
# represent echo nest call (artist and/or song)
# contains rest API consumption code
# need a better name

# echo nest call
# URL = LEAD + VERSION + TYPE + METHOD + '?' + KEY + ...
class ENC:
    LEAD = "http://developer.echonest.com/api/"
    VERSION = "v4/"
    KEY = "api_key=QZQG43T7640VIF4FN"
    FORMAT = "&format=json" # request header might handle this

    # constructor will form a url string up to the type (artist or song)
    # different calls (like get most popular artists / get top artist songs / etc will be created in build(**args)
    def __init__(self, method, artist_id=None, song_id=None):
        if not artist_id and not song_id:
            raise EmptyCall('EchoNest calls require an artist or song id.') # place in except msg

        self.METHOD = method + "/"

        if artist_id:
            self.TYPE = "artist/"
        else:
            self.TYPE = "song/"

    # build api url using buckets
    # def build(self, **kwargs):
    # do not modify self vars
    def build(self, params):
        if not kwargs:
            raise EmptyQuery('No parameters specified.') # place in except msg

        # self.URL = LEAD + VERSION + TYPE + METHOD + "?" + KEY + FORMAT
        url = LEAD + VERSION + TYPE + METHOD + "?"

        # parse params dict for invalid keys


        return self.url

    # consume call and return JSON (should we catch access limit except here?)
    def consume(self):



        data = urllib.urlencode(data)
        data = "&".join([data, params])
        urllib.quote(string)

        return

# expand
class EmptyCall(Exception):
    pass
class EmptyQuery(Exception):
    pass

#======================================================================================================
    # http://developer.echonest.com/api/v4/artist/search?api_key=YOUR_API_KEY&format=json&name=radiohead&results=1
    # http://developer.echonest.com/api/v4/song/search?api_key=YOUR_API_KEY&format=json&results=1&artist=radiohead&title=karma%20police

# def test_api(request):
#     query = request.GET['q']

#     import requests
#     url = 'http://developer.echonest.com/api/v4/artist/hotttnesss'
#     key = 'QZQG43T7640VIF4FN'
#     data = {
#         'api_key': key,
#         'name': 'the beatles'
#     }
#     headers = {'Content-type': 'application/json'}
#     data = requests.request('GET', url, params=data, headers=headers)

#     j = data.json()

#     return HttpResponse(json.dumps(j), content_type="application/json")
