from django.shortcuts import render
from django.template import RequestContext, loader, Context
from pyechonest import config, artist

def index(request):
    return render(request, 'index.html')

def search(request):
    config.ECHO_NEST_API_KEY="REMOVED"

    s_artist = request.GET['q']
    s_results = artist.search(name=s_artist)

    c = Context({'s_results': s_results})


    return render(request, 'result.html', c)