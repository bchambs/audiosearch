from django.shortcuts import render
from django.template import RequestContext, loader, Context
from pyechonest import config, artist, song
from operator import itemgetter

def index(request):
    return render(request, 'index.html')

def search(request):
    #removed for security, add your key
    config.ECHO_NEST_API_KEY="ULIQ4Q3WGU8MM4W2F"

    qs = request.GET['q']
    
    artists = artist.search(name=qs, sort='hotttnesss-desc', results=10)
    songs = song.search(title=qs, sort='song_hotttnesss-desc', results=10)

    c = Context({
    	'artists': artists,
    	'songs': songs,
    })

    return render(request, 'result.html', c)