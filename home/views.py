from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from pyechonest import config, artist, song, track
from random import choice
from util import *

#globals
config.ECHO_NEST_API_KEY=""

#store featured artist as global to reduce our API call count
#this is hacky and needs to replaced with a server startup script
#maybe set this in an EV; that could be terrible I don't know...
_featured_artist = 'M83'
_featured_terms = []
_featured_bio = ''
_initialized = False

#store index trending so front page never displays 500
_index_trending = []

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
        featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]
        _featured_bio = get_good_bio (featured_artist.biographies, 200, 9999)

        #ensure we have 2 terms
        #needs error checking, what if artist does not have terms?
        _featured_terms.append(featured_artist.terms[0]['name'])
        _featured_terms[0] += ', '
        _featured_terms.append(featured_artist.terms[1]['name'])

        #get displayable bio
        _featured_bio = get_good_bio (featured_artist.biographies, 200, 9999)
        _featured_bio = _featured_bio[:197] + '...'

        #populate trending artists for index
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
    context = Context({})

    #results is 1 when we have something to display
    if query:

        #search for 35 artists and trim duplicates
        artists = artist.search(name=query, sort='hotttnesss-desc', results=35)
        trimmed_artists = remove_duplicate_artists(artists, 10)
        context['artists'] = trimmed_artists

        #search for 35 songs and trim duplicates
        songs = song.search(title=query, sort='song_hotttnesss-desc', results=35)
        trimmed_songs = remove_duplicate_songs(songs, 10)
        context['songs'] = trimmed_songs

        if artists or songs:
            context['results'] = 1
        else:
            context['results'] = 0

    else: 
        context['results'] = 0

    context['featured_name'] = _featured_artist

    return render(request, 'result.html', context)

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

    trending = artist.top_hottt()
    del trending[10:]

    top_songs = remove_duplicate_songs (trending[0].songs, 3)

    context = Context({
        "top_songs": top_songs,
        "trending": trending,
        "featured_name": _featured_artist,
    })

    return render (request, 'trending.html', context)

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
            context['artists']= remove_duplicate_artists(s_artist.similar, 10)

        if s_artist.biographies:
            bios = s_artist.get_biographies(results=20)
            good_bio = get_good_bio(bios, 150, 9999)
            good_bio = good_bio[:350] + '...'
            context['bio'] = good_bio

        context['name']= s_artist.name
        context['hot']= s_artist.hotttnesss
        context['songs']= remove_duplicate_songs(s_artist.get_songs(results=50), 10)

    else:
        context['results'] = False

    return render(request, 'artist.html', context)

def song_info(request):
    global _featured_artist

    query = request.GET['q']
    context = Context({})

    context['featured_name'] = _featured_artist

    s_song_temp = song.search(title=query, sort='song_hotttnesss-desc', results=1)

    # if s_song_temp:
    #     temp_artist = artist.search(name=s_song_temp[0].artist_name, sort='hotttnesss-desc', results=1)

    # if s_song_temp and temp_artist:
    if s_song_temp:
        s_song = s_song_temp[0]
        context['results'] = True

        # if temp_artist[0].similar:
        #     similar_artists = temp_artist[0].similar[:10]

        # similar_songs = get_similar_songs(similar_artists)

        context['title'] = s_song.title
        context['artist'] = s_song.artist_name
        context['hot'] = s_song.song_hotttnesss
        # context['similar_songs'] = similar_songs
        # context['similar_artists'] = similar_artists

        #get song facts from audio dict
        context['dance'] = s_song.audio_summary['danceability']
        context['duration'] = s_song.audio_summary['duration']
        context['energy'] = s_song.audio_summary['energy']
        context['liveness'] = s_song.audio_summary['liveness']
        context['speechiness'] = s_song.audio_summary['speechiness']

    else:
        context['results'] = False

    return render(request, 'song.html', context)

def server_error(request):
    response = render(request, "500.html")
    response.status_code = 500
    return response