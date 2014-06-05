from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from pyechonest import config, artist, song
from random import choice
from util import *
from django.utils.safestring import mark_safe

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
        a = artist.Artist (s.artist_id, buckets=[])

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
    global _featured_artist

    query = request.GET['q']
    context = Context({})
    context['featured'] = _featured_artist

    a = artist.Artist (query, buckets=['biographies', 'hotttnesss', 'images', 'terms'])

    if a:
        context['display'] = True

        if a.images:
            image = choice(a.images)['url']
            context['image'] = image
            context['image_src'] = mark_safe("\"" + image + "\"")   # allows us to pass url as a string to js function

        if a.terms:
            terms = []

            if len(a.terms) > 2:
                terms.append(a.terms[0]['name'])
                terms[0] += ", "                    # add this on template (?)
                terms.append(a.terms[1]['name'])

            elif len(a.terms) > 1:
                terms.append(a.terms[0]['name'])
            else:
                terms.append("Unknown")
            
            context['terms'] = terms

        if a.biographies:
            short = 800;

            bio = get_good_bio(a.biographies)
            context['long_bio'] = bio
            context['short_bio'] = bio[:short] + '...'

        context['name'] = a.name
        context['hot'] = a.hotttnesss
        context['twitter'] = a.get_twitter_id
        context['artists'] = a.similar[:10]

        songs = song.search(artist_id=a.id, sort='song_hotttnesss-desc', results=35)
        context['songs'] = remove_duplicates(songs, 10)

    else:
        context['display'] = False

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
        "featured": _featured_artist,
    })

    return render (request, 'about.html', context)




def trending(request):
    global _featured_artist

    context = Context({})
    trending = artist.search(sort='hotttnesss-desc', results=10, buckets=['hotttnesss', 'images', 'songs', 'terms'])

    #REMOVE DUPLICATES

    if trending:
        if len (trending[0].songs) < 3:
            top_count = len (trending[0].songs)
        else:
            top_count = 3

        top_songs = trending[0].songs[0:3]

        context['top_songs'] = top_songs
        context['trending'] = trending
        context['featured'] = _featured_artist

    return render (request, 'trending.html', context)




def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response



######
#NOTES
######
#
# 1. is it better to pass song / artist objects to context dict, or define every field is a key / value pair?
#   :succinct back-end code vs abstraction.  abstraction is probably faster (?)
# 2. done
# 3. make remove_duplicates check artist_id (?), add to trending / song / artist / result pages
# 4. fix featured artist not using id
# 5. make qstrings prettier (?)
# 6. fix stretched images
# 7. have failed compare redirect to /compare/ with the footer
# 8. remake trending template
