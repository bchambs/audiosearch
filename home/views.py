from django.shortcuts import render
from django.template import RequestContext, loader, Context
from django.http import HttpResponseRedirect
from pyechonest import config, artist, song, track
from random import choice
from util import *

#globals
config.ECHO_NEST_API_KEY="ULIQ4Q3WGU8MM4W2F"
_featured_artist = "M83"

def index(request):
    trending = artist.top_hottt()
    del trending[10:]

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    #ensure we have 2 terms
    #needs error checking, what if artist does not have terms?
    featured_terms = []
    featured_terms.append(featured_artist.terms[0]['name'])
    featured_terms[0] += ', '
    featured_terms.append(featured_artist.terms[1]['name'])

    #get displayable bio
    featured_bio = get_good_bio (featured_artist.biographies)

    context = Context({
        'trending': trending,
        'featured_name': featured_artist.name,
        'featured_terms': featured_terms,
        'featured_bio': featured_bio,
    })

    return render(request, 'index.html', context)

def search(request):
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

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]
    context['featured_name'] = featured_artist.name

    return render(request, 'result.html', context)

def compare(request):
    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        "featured_name": featured_artist.name,
    })

    return render(request, 'compare.html', context)

def compare_results(request):
    query = request.GET['q']
    query_2 = request.GET['q2']
    context = Context({})

    #fill context with song 1 and song 2 data
    if query and query_2:
        song_one = song.search(title=query, sort='song_hotttnesss-desc', results=1)[0]
        context['title_one'] = song_one.title
        context['artist_one'] = song_one.artist_name
        context['hot_one'] = song_one.song_hotttnesss
        context['dance_one'] = song_one.audio_summary['danceability'],
        context['duration_one'] = song_one.audio_summary['duration'],
        context['energy_one'] = song_one.audio_summary['energy'],
        context['liveness_one'] = song_one.audio_summary['liveness'],
        context['speechiness_one'] = song_one.audio_summary['speechiness'],

        song_two = song.search(title=query_2, sort='song_hotttnesss-desc', results=1)[0]
        context['title_two'] = song_two.title
        context['artist_two'] = song_two.artist_name
        context['hot_two'] = song_two.song_hotttnesss
        context['dance_two'] = song_two.audio_summary['danceability'],
        context['duration_two'] = song_two.audio_summary['duration'],
        context['energy_two'] = song_two.audio_summary['energy'],
        context['liveness_two'] = song_two.audio_summary['liveness'],
        context['speechiness_two'] = song_two.audio_summary['speechiness'],

        featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]
        context['featured_name'] = featured_artist.name,

        return render(request, 'compare-results.html', context)

    else:
        return HttpResponseRedirect('/compare/')

def about(request):
    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        "featured_name": featured_artist.name,
    })

    return render (request, 'about.html', context)

def trending(request):
    trending = artist.top_hottt()
    del trending[10:]

    top_songs = remove_duplicate_songs (trending[0].songs, 3)
    print len(trending[0].songs)

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        "top_songs": top_songs,
        "trending": trending,
        "featured_name": featured_artist.name,
    })

    return render (request, 'trending.html', context)

def artist_info(request):
    query = request.GET['q']
    context = Context({})

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    #set artist to first in list
    s_artist = artist.search(name=query)[0]

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
        context['bio']= s_artist.biographies[0]['text']

    context['name']= s_artist.name
    context['hot']= s_artist.hotttnesss
    context['songs']= remove_duplicate_songs(s_artist.get_songs(results=35), 10)
    context['featured_name']= featured_artist.name

    return render(request, 'artist.html', context)

def song_info(request):
    query = request.GET['q']

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    #set song to first in list
    s_song = song.search(title=query, sort='song_hotttnesss-desc', results=1)[0]
    temp_artist = artist.search(name=s_song.artist_name, sort='hotttnesss-desc', results=1)[0]

    similar_artists = temp_artist.similar[:10]
    similar_songs = get_similar_songs(similar_artists)

    context = Context({
        'title':s_song.title,
        'artist':s_song.artist_name,
        'hot':s_song.song_hotttnesss,
        'similar_songs': similar_songs,
        'similar_artists': similar_artists,

        #get song facts from audio dict
        'dance':s_song.audio_summary['danceability'],
        'duration':s_song.audio_summary['duration'],
        'energy':s_song.audio_summary['energy'],
        'liveness':s_song.audio_summary['liveness'],
        'speechiness':s_song.audio_summary['speechiness'],

        'featured_name': featured_artist.name,
    })
    
    # try to get song data that I can graph with javascript
    # it's not working for some reason
    # tracks = s_song.get_tracks('7digital-US')[0]
    # print tracks['id']
    # print s_song.id
    # t = track.track_from_ud(tracks['id'])
    # t.get_analysis(t)

    # try:
    #     info = t.get_analysis()
    #     print "beats"
    #     print info.beats
    #     print "samples"
    #     print info.num_samples
    #     print "sections"
    #     print info.sections
    #     print "segments"
    #     print info.segments
    #     print
    # except:
    #     print
    #     print "UNABLE TO READ SONG DATA"
    #     print

    return render(request, 'song.html', context)
