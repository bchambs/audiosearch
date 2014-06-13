import unicodedata
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
from event_queue import *
from worker import *

import redis

# globals
config.ECHO_NEST_API_KEY='QZQG43T7640VIF4FN'
event_queue = EventQueue()
# redis = redis.StrictRedis(host='localhost', port=6379, db=0)

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
    global event_queue

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
        w1 = Worker(event_queue)
        w1.start()
        


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


def search(request):
    global _featured_artist

    query = request.GET['q']
    query = query.rstrip()
    context = Context({})

    if query:
        artists = artist.search(name=query, sort='hotttnesss-desc', results=10)
        context['artists'] = artists

        songs = song.search(title=query, sort='song_hotttnesss-desc', results=35)
        context['songs'] = remove_duplicates(songs, 10)

        # print "none found" if false
        if artists or songs:
            context['display'] = True
        else:
            context['display'] = False

    else: 
        context['display'] = False

    context['featured'] = _featured_artist

    return render(request, 'result.html', context)


def song_info(request):
    global _featured_artist

    query = request.GET['q']
    context = Context({})

    context['featured'] = _featured_artist

    s = song.Song (query, buckets=['song_hotttnesss', 'audio_summary'])

    if s:
        context['display'] = True

        # check and populate similar artists
        a = artist.Artist (s.artist_id)

        if a:
            sim_artists = a.similar[:10]
            sim_songs = get_similar_songs(sim_artists)

            context['similar_artists'] = sim_artists
            context['similar_songs'] = sim_songs[:10]

        context['title'] = s.title
        context['artist'] = s.artist_name
        context['artist_id'] = s.artist_id
        context['hot'] = s.song_hotttnesss

        #get facts from audio dict
        context['dance'] = s.audio_summary['danceability']
        context['duration'] = s.audio_summary['duration']
        context['energy'] = s.audio_summary['energy']
        context['liveness'] = s.audio_summary['liveness']
        context['speechiness'] = s.audio_summary['speechiness']

    else:
        context['display'] = False

    return render(request, 'song.html', context)













def artist_info(request):
    query = request.GET['q']
    context = Context({})

    req = Request(query)
    event_queue.enqueue(req)

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














def compare(request):
    global _featured_artist

    context = Context({
        "featured": _featured_artist,
    })

    return render(request, 'compare.html', context)


def compare_results(request):
    global _featured_artist

    query = request.GET['q']
    query2 = request.GET['q2']
    context = Context({})

    context['featured'] = _featured_artist,

    if query and query2:
        # search for songs, find their id, create song objects if they exist
        song_one = song.search(title=query, sort='song_hotttnesss-desc', results=1)
        song_two = song.search(title=query2, sort='song_hotttnesss-desc', results=1)
        one = None
        two = None

        if song_one:
            one = song.Song (song_one[0].id, buckets=['song_hotttnesss', 'audio_summary'])

        if song_two:
            two = song.Song (song_two[0].id, buckets=['song_hotttnesss', 'audio_summary'])

        # if both songs exist, populate context
        if one and two:
            context['display'] = True

            # one
            context['one_title'] = one.title
            context['one_artist'] = one.artist_name
            context['one_id'] = one.id
            context['one_artist_id'] = one.artist_id
            context['one_hot'] = one.song_hotttnesss
            context['one_dance'] = one.audio_summary['danceability']
            context['one_duration'] = one.audio_summary['duration']
            context['one_energy'] = one.audio_summary['energy']
            context['one_liveness'] = one.audio_summary['liveness']
            context['one_speechiness'] = one.audio_summary['speechiness']

            # two
            context['two_title'] = two.title
            context['two_artist'] = two.artist_name
            context['two_id'] = two.id
            context['two_artist_id'] = two.artist_id
            context['two_hot'] = two.song_hotttnesss
            context['two_dance'] = two.audio_summary['danceability']
            context['two_duration'] = two.audio_summary['duration']
            context['two_energy'] = two.audio_summary['energy']
            context['two_liveness'] = two.audio_summary['liveness']
            context['two_speechiness'] = two.audio_summary['speechiness']

            return render(request, 'compare-results.html', context)
        else:
            context['display'] = False

        return render(request, 'compare-results.html', context)

    else:
        return HttpResponseRedirect('/compare/')


def about(request):
    global _featured_artist

    context = Context({
        "featured": _featured_artist
    })

    return render (request, 'about.html', context)


def trending(request):
    global _featured_artist

    context = Context({})
    trending = artist.search(sort='hotttnesss-desc', results=10, buckets=['hotttnesss', 'images', 'songs', 'terms'])

    if trending:
        if len (trending[0].songs) < 3:
            top_count = len(trending[0].songs)
        else:
            top_count = 3

        top_songs = remove_duplicates(trending[0].songs, top_count)

        context['top_songs'] = top_songs
        context['trending'] = trending
        context['featured'] = _featured_artist

    return render (request, 'trending.html', context)

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

######
#NOTES
######

# 5. make qstrings prettier (?)
# 7. have failed compare redirect to /compare/ with the footer
# 8. remake trending template
# 9. during redesign: remove 'display' key from /compare-results/.  when one artist is not found, add 'display' key to request object and redirect to /compare/
