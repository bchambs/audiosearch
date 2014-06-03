from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from pyechonest import config, artist, song, track
from random import choice
from util import *

# globals
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
        _featured_bio = get_good_bio (featured_artist.biographies, bio_min, bio_max)

        # get terms
        if len(featured_artist.terms) > 1:
            _featured_terms.append(featured.terms[0]['name'])
        if len(featured_artist.terms) > 2:
            _featured_terms[0] += ', '
            _featured_terms.append(featured.terms[1]['name'])
        else:
            _featured_terms.append ('Unknown')

        # get displayable bio
        _featured_bio = get_good_bio (featured_artist.biographies, bio_min, bio_max)
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




def search(request):
    global _featured_artist

    query = request.GET['q']
    query = query.rstrip()
    context = Context({})

    if query:
        artists = artist.search(name=query, sort='hotttnesss-desc', results=10)
        context['artists'] = artists

        songs = song.search(title=query, sort='song_hotttnesss-desc', results=10)
        context['songs'] = songs

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
        a = artist.Artist (s.artist_id, buckets=[])

        if a:
           sim_artists = a.similar[:10]
           sim_songs = get_similar_songs(sim_artists)

           context['similar_artists'] = sim_artists
           context['similar_songs'] = sim_songs[:10]

        context['title'] = s.title
        context['artist'] = s.artist_name
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
    global _featured_artist

    query = request.GET['q']
    context = Context({})
    context['featured_name']= _featured_artist

    #set artist to first in list
    s_artist_temp = artist.search(name=query, results=1, buckets=['biographies', 'hotttnesss', 'images', 'songs', 'terms'])

    if s_artist_temp:
        context['results'] = True
        s_artist = s_artist_temp[0]

        #see if artist data exists, add to dict if true
        if s_artist.images:
            context['image']= choice(s_artist.images)['url']

        if s_artist.terms:
            terms = []
            if len(s_artist.terms) > 1:
                terms.append(s_artist.terms[0]['name'])
                terms[0] += ", "
                terms.append(s_artist.terms[1]['name'])
            else:
                terms.append(s_artist.terms[0]['name'])
            
            context['terms']= terms

        if s_artist.get_twitter_id:
            context['twitter']= s_artist.get_twitter_id

        if s_artist.similar:
            #context['artists']= remove_duplicate_artists(s_artist.similar, 10)
            context['artists']= remove_duplicates(s_artist.similar, 10)

        if s_artist.biographies:
            bios = s_artist.get_biographies(results=20)
            good_bio = get_good_bio(bios, 150, 9999)
            good_bio = good_bio[:350] + '...'
            context['bio'] = good_bio

        context['name']= s_artist.name
        context['hot']= s_artist.hotttnesss
        #context['songs']= remove_duplicate_songs(s_artist.get_songs(results=50), 10)
        context['songs']= remove_duplicates(s_artist.get_songs(results=50), 10)

    else:
        context['results'] = False

    return render(request, 'artist.html', context)




def compare(request):
    global _featured_artist

    context = Context({
        "featured_name": _featured_artist,
    })

    return render(request, 'compare.html', context)




def compare_results(request):
    global _featured_artist

    query = request.GET['q']
    query_2 = request.GET['q2']
    context = Context({})

    context['featured_name'] = _featured_artist,

    #fill context with song 1 and song 2 data
    if query and query_2:
        song_one_temp = song.search(title=query, sort='song_hotttnesss-desc', results=1)
        song_two_temp = song.search(title=query_2, sort='song_hotttnesss-desc', results=1)

        #see if each song has info, if not redirect to compare
        if song_one_temp and song_two_temp:
            song_one = song_one_temp[0]
            song_two = song_two_temp[0]

            context['results'] = True

            context['title_one'] = song_one.title
            context['artist_one'] = song_one.artist_name
            context['hot_one'] = song_one.song_hotttnesss
            context['dance_one'] = song_one.audio_summary['danceability']
            context['duration_one'] = song_one.audio_summary['duration']
            context['energy_one'] = song_one.audio_summary['energy']
            context['liveness_one'] = song_one.audio_summary['liveness']
            context['speechiness_one'] = song_one.audio_summary['speechiness']

            song_two = song.search(title=query_2, sort='song_hotttnesss-desc', results=1)[0]
            context['title_two'] = song_two.title
            context['artist_two'] = song_two.artist_name
            context['hot_two'] = song_two.song_hotttnesss
            context['dance_two'] = song_two.audio_summary['danceability']
            context['duration_two'] = song_two.audio_summary['duration']
            context['energy_two'] = song_two.audio_summary['energy']
            context['liveness_two'] = song_two.audio_summary['liveness']
            context['speechiness_two'] = song_two.audio_summary['speechiness']

            return render(request, 'compare-results.html', context)
        else:
            context['results'] = False

        return render(request, 'compare-results.html', context)

    else:
        return HttpResponseRedirect('/compare/')




def about(request):
    global _featured_artist

    context = Context({
        "featured_name": _featured_artist,
    })

    return render (request, 'about.html', context)




def trending(request):
    global _featured_artist

    trending = artist.search(sort='hotttnesss-desc', results=10, buckets=['hotttnesss', 'images', 'songs', 'terms'])

    #top_songs = remove_duplicate_songs (trending[0].songs, 10)
    top_songs = remove_duplicates (trending[0].songs, 10)

    context = Context({
        "top_songs": top_songs,
        "trending": trending,
        "featured_name": _featured_artist,
    })

    return render (request, 'trending.html', context)




def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response