from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'src.views.index'),   

    url(r'^music/(artist)$', 'src.views.artist'),

    # url(r'^artist/$', 'src.views.artist'),
    url(r'^ajax/$', 'src.views.retrieve_resource'),
    
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler500 = 'src.views.server_error'
