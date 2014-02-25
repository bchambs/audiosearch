from django.shortcuts import render
from django.template import RequestContext, loader, Context
from pyechonest import config, artist, song
from random import choice

#############################
# CATCH EMPTY QUERY STRINGS #
#############################

def index(request):
    return render(request, 'index.html')

def search(request):
    #removed for security, add your key
    config.ECHO_NEST_API_KEY=""

    c = Context({})

    #this still breaks on empty query string fix it
    if 'q' in request.GET:
        qs = request.GET['q']
    
        #get sorted list of artists and songs
        artists = artist.search(name=qs, sort='hotttnesss-desc', results=10)
        songs = song.search(title=qs, sort='song_hotttnesss-desc', results=10)

        c = {
            'artists': artists,
            'songs': songs,
        }

    return render(request, 'result.html', c)

def artist_info(request):
    qs = request.GET['q']

    #set artist to first in list
    a = artist.search(name=qs)[0] #why dont buckets work....
    i = choice(a.images)
    t = a.get_twitter_id

    c = Context({
        'name': a.name,
        'similar': a.similar, 
        'hot': a.hotttnesss,
        'image': i['url'],
        'twitter': t,
    })

    return render(request, 'artist.html', c)

def song_info(request):
    qs = request.GET['q']

    #set song to first in list
    s = song.search(title=qs)[0]

    c = Context({
        'title': s.title,
        'artist': s.artist_name,
        'hot': s.song_hotttnesss,
        'duration': s.audio_summary['duration'],
        'speechiness': s.audio_summary['speechiness'],
        'tempo': s.audio_summary['tempo'],
    })

    return render(request, 'song.html', c)