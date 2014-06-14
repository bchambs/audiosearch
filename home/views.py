import json
import threading
from time import *
from random import choice

from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect, HttpResponse

from pyechonest import config, artist, song
from pyechonest.util import EchoNestAPIError

from util import *
from request import *

import tasks

config.ECHO_NEST_API_KEY='QZQG43T7640VIF4FN'

# store featured artist as global to reduce our API call count
# this is hacky and needs to replaced.  
_featured_artist = 'M83'
_featured_terms = []
_featured_bio = ''
_initialized = False

# store index trending so front page never displays 500
_index_trending = []

# consider delegating this data population to a script which 
# is scheduled to run at X rate (hourly?).  save results to
# a file, and have an update function run to populate the index dictionary
# ! -> is I/O on the index worth it?
def startup():
    global _initialized
    global _featured_artist
    global _featured_terms
    global _featured_bio
    global _index_trending

    if not _initialized:
        print
        print '_____________________________________________________________________'
        print 'Initializing index. This should not happen more than once per deploy.'
        print

        _initialized = True
        bio_min = 200
        bio_max = 3000

        featured = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

        # get terms
        if len(featured.terms) > 2:
            _featured_terms.append(featured.terms[0]['name'])
            _featured_terms[0] += ', '
            _featured_terms.append(featured.terms[1]['name'])

        elif len(featured.terms) > 1:
            _featured_terms.append(featured.terms[0]['name'])
        else:
            _featured_terms.append ('Unknown')

        # get displayable bio
        _featured_bio = get_good_bio (featured.biographies)
        _featured_bio = _featured_bio[:bio_min] + '...'

        # populate trending artists
        _index_trending = artist.top_hottt()
        del _index_trending[10:]
        


def index(request):
    global _index_trending
    global _featured_bio
    global _featured_artist
    global _featured_terms

    startup()

    context = Context({
        'trending': _index_trending,
        'featured_name': _featured_artist,
        'featured_terms': _featured_terms,
        'featured_bio': _featured_bio,
    })

    return render(request, 'index.html', context)



def artist_info(request):
    query = request.GET['q']
    context = Context({})

    req = Request(query)

    tasks.defer_request.delay()

    context['served'] = False

    return render(request, 'artist.html', context)
    # end test=================================================

    # attempt to request echo nest data, catch limit exception
    try:
        artist_ = artist.Artist(query, buckets=['biographies', 'hotttnesss', 'images', 'terms'])
        songs = song.search(artist_id=artist_.id, sort='song_hotttnesss-desc', results=35)

        # pass context as param to avoid combining both dicts
        map_artist_context(artist_, context)
        map_song_context(songs, context)

        return render(request, 'artist.html', context)

    # defer the request, return an empty page, then do an async request
    except EchoNestAPIError:
        # thread = threading.Thread(target=defer_request, args=(query))
        # thread.start()

        context['served'] = False

        return render(request, 'artist.html', context)



# serves 500 pages
def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response

# will continuously 
# def defer_request(query):
    


def obtain_request(id):
    data = {}
    return HttpResponse(json.dumps(data), content_type="application/json")
