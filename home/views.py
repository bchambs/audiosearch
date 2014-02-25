from django.shortcuts import render
from django.template import RequestContext, loader, Context
from pyechonest import config, artist, song

def index(request):
    return render(request, 'index.html')

def search(request):
    #removed for security, add your key
    config.ECHO_NEST_API_KEY="ULIQ4Q3WGU8MM4W2F"

    c = Context({})

    if 'q' in request.GET:
        qs = request.GET['q']
    
        artists = artist.search(name=qs, sort='hotttnesss-desc', results=10)
        songs = song.search(title=qs, sort='song_hotttnesss-desc', results=10)

        c = {
            'artists': artists,
            'songs': songs,
        }

    return render(request, 'result.html', c)

def artist_info(request):
    qs = request.GET['q']

    c = Context({})
    return render(request, 'artist.html', c)

def song_info(request):
    qs = request.GET['q']

    c = Context({})
    return render(request, 'song.html', c)