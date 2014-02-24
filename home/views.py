from django.shortcuts import render
from django.template import RequestContext, loader, Context
from pyechonest import config, artist, song
from util import *

def index(request):
    return render(request, 'index.html')

def search(request):
    #removed for security, add your key
    config.ECHO_NEST_API_KEY="ULIQ4Q3WGU8MM4W2F"

    weezer_results = artist.search(name='weezer')

    c = Context({})

    if 'q' in request.GET:
        qs = request.GET['q']
    
        artists = artist.search(name=qs, sort='hotttnesss-desc', results=10)
        songs = song.search(title=qs, sort='song_hotttnesss-desc', results=10)
        artists_urls = [0] * len(artists)

        for x in range(0,len(artists)):
            artists_urls[x] = fix_spaces (artists[x].name)

        c = {
            'artists': artists,
            'songs': songs,
            'artists_urls': artists_urls,
        }

    return render(request, 'result.html', c)

def artist_info(request):
    qs = request.GET['q']

    c = Context({})
    return render(request, 'artist.html', c)

def song_info(request):
    c = Context({})

    return render(request, 'song.html', c)