from django.shortcuts import render
from django.template import RequestContext, loader, Context
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

    artists = artist.search(name=query, sort='hotttnesss-desc', results=10)
    songs = song.search(title=query, sort='song_hotttnesss-desc', results=10)
    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        'artists': artists,
        'songs': songs,
        'featured_name': featured_artist.name,
    })

    return render(request, 'result.html', context)

def compare(request):
    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        "featured_name": featured_artist.name,
    })

    return render(request, 'compare.html', context)

def about(request):
    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        "featured_name": featured_artist.name,
    })

    return render (request, 'about.html', context)

def trending(request):
    trending = artist.top_hottt()
    del trending[10:]

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    context = Context({
        "featured_name": featured_artist.name,
        "trending": trending,
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
        context['similar']= remove_duplicate_artists(s_artist.similar, 10)

    if s_artist.biographies:
        context['bio']= s_artist.biographies[0]['text']

    context['name']= s_artist.name
    context['hot']= s_artist.hotttnesss
    context['songs']= remove_duplicate_songs(s_artist.songs, 10)
    context['featured_name']= featured_artist.name

    return render(request, 'artist.html', context)

def song_info(request):
    query = request.GET['q']

    featured_artist = artist.search(name=_featured_artist, sort='hotttnesss-desc', results=1)[0]

    #set song to first in list
    s_song = song.search(title=query, sort='song_hotttnesss-desc', results=1)[0]

    context = Context({
        'title':s_song.title,
        'artist':s_song.artist_name,
        'hot':s_song.song_hotttnesss,
        'id':s_song.id,

        #get song facts from audio dict
        'dance':s_song.audio_summary['danceability'],
        'duration':s_song.audio_summary['duration'],
        'energy':s_song.audio_summary['energy'],
        'liveness':s_song.audio_summary['liveness'],
        'loudness':s_song.audio_summary['loudness'],
        'speechiness':s_song.audio_summary['speechiness'],
        'tempo':s_song.audio_summary['tempo'],

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
