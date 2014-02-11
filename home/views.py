from django.shortcuts import render
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from forms import single_music_form

def index (request):
    if request.method == 'POST': # If the form has been submitted...
        form = single_music_form(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            
			
			
            return HttpResponseRedirect('/result/') # Redirect after POST
    else:
        form = single_music_form() # An unbound form

    return render(request, 'index.html', {
        'form': form,
    })