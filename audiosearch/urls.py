from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'src.views.index'),   
    url(r'^search/$', 'src.views.search'),
    url(r'^artist/$', 'src.views.artist_info'),
    url(r'^song/$', 'src.views.song_info'),
    # url(r'^about/$', 'src.views.about'),
    # url(r'^compare/$', 'src.views.compare'),
    # url(r'^compare_results/$', 'src.views.compare_results'),
    # url(r'^trending/$', 'src.views.trending'),

    url(r'^artistjx/$', 'src.views.async_artist'),
    
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler500 = 'src.views.server_error'
