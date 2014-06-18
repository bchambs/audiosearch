import json
import requests
import urllib

__all__ = ['ENCall']

# Echo Nest call
# URL = LEAD + VERSION + TYPE + METHOD + '?' + KEY + ...
class ENCall:
    LEAD = "http://developer.echonest.com/api/"
    VERSION = "v4/"
    CTYPE = ''
    METHOD = ''
    KEY = "api_key=QZQG43T7640VIF4FN"
    FORMAT = "&format=json"


    # constructor will form a url string up to the method (artist or song)
    # different calls (like get most popular artists / get top artist songs / etc will be created in build(**args)
    def __init__(self, call_type, method):
        self.METHOD = method

        if call_type is 'artist' :
            self.CTYPE = "artist/"
        elif call_type is 'song':
            self.CTYPE = "song/"
        else:
            raise InvalidCallType('Call type must be artist or song.')


    # build REST call using buckets
    # return complete url
    def build(self, EN_id, params):
        if not EN_id or not params:
            raise EmptyQuery('No parameters specified.')

        url = self.LEAD + self.VERSION + self.CTYPE + self.METHOD + "?" + self.KEY + self.FORMAT + "&id=" + EN_id
        for p in params:
            url += '&bucket=' + str(p)

        print
        print url
        print

        return url

    # consume call and return JSON
    @staticmethod
    def consume(url):



        data = urllib.urlencode(data)
        data = "&".join([data, params])
        urllib.quote(string)

        return

# expand
class InvalidCallType(Exception):
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
