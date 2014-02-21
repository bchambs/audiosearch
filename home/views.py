from django.shortcuts import render
from django.template import RequestContext, loader, Context
from pyechonest import config, artist

def index(request):
    return render(request, 'index.html')

def search(request):
	#removed for security, add your key
    config.ECHO_NEST_API_KEY="REMOVED"

    s_artist = request.GET['q']
    s_results = artist.search(name=s_artist)
    first = s_results[0]

    #print details of first match
    c = Context({
        'name': first.name,
        'active': first.years_active, 
        'hot': first.hotttnesss,
        'songs': first.get_songs(results=25),
        'similar': first.similar,
    })

    return render(request, 'result.html', c)