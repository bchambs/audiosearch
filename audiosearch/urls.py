from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index'),   
    url(r'^search/$', 'home.views.search'),
    url(r'^artist/$', 'home.views.artist_info'),
    url(r'^song/$', 'home.views.song_info'),
    url(r'^about/$', 'home.views.about'),
    url(r'^compare/$', 'home.views.compare'),
    url(r'^compare_results/$', 'home.views.compare_results'),
    url(r'^trending/$', 'home.views.trending'),

    url(r'^artistjx/$', 'home.views.async_artist'),
    
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler500 = 'home.views.server_error'
