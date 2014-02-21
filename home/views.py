from django.shortcuts import render
from django.template import RequestContext, loader, Context

def index(request):
    return render(request, 'index.html')

def search(request):
    c = Context({'qstring': request.GET['q']})

    return render(request, 'result.html', c)