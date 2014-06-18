import json
import requests
import urllib

__all__ = ['ENCall']

# Echo Nest call
class ENCall:
    LEAD = "http://developer.echonest.com/api"
    VERSION = "v4"
    KEY = ("api_key", "QZQG43T7640VIF4FN")
    FORMAT = ("format", "json")


    # form url without query string
    def __init__(self, call_type, method):
        self.ctype = call_type
        self.method = method
        self.path = '/'.join([ENCall.LEAD, ENCall.VERSION, self.ctype, self.method])


    # return consumable url
    # elements of url are stored tuples for .join.  we don't need ordered dicts (at this time)
    def build(self, EN_id, params):
        param_list = [
            ENCall.KEY,
            ENCall.FORMAT,
            ("id", EN_id)
        ]

        param_list.extend( [('bucket', p) for p in params] )
        query = urllib.urlencode(param_list)

        return '?'.join( (self.path, query) )


    # consume call and return JSON
    @staticmethod
    def consume(url):
        
        
        return


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
