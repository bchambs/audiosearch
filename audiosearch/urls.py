from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'src.views.index'),   
    url(r'^search/$', 'src.views.search'),
    url(r'^search/artists$', 'src.views.more_artists_results'),

    # url(r'^search/$', 'src.views.search'),
    # url(r'^search/$', 'src.views.search'),

    
    url(r'^artist/$', 'src.views.artist_info'),
    url(r'^song/$', 'src.views.song_info'),
    # url(r'^about/$', 'src.views.about'),
    # url(r'^trending/$', 'src.views.trending'),

    url(r'^ajax/$', 'src.views.retrieve_resource'),
    
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler500 = 'src.views.server_error'
