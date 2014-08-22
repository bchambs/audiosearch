from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.http import HttpResponse

from src import views


urlpatterns = patterns('',

    # General.
    url(ur'^$', views.index), 
    url(ur'^about/$', views.about),
    url(ur'^search/$', views.search, {'cache_prefix': 'search'}),
    url(ur'^music/$', views.music_home, {'cache_prefix': 'top'}),
    url(ur'^trending/$', views.trending, {'cache_prefix': 'trending'}),


    # Songs.
    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/\+similar/$', views.song_content, {
        'content_key': 'song_playlist', 
        'description': "Similar Songs",
        'cache_prefix': 'song',
        }),
    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/\+recommended/$', views.song_content, {
        'content_key': 'similar_artists', 
        'description': "Recommended Artists",
        'cache_prefix': 'song',
        }),
    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/$', views.song_home, {'cache_prefix': 'song'}),


    # Artists.
    url(ur'^music/(?P<artist>(?!/_/).*)/\+similar/$', views.artist_content, {
        'content_key': 'similar_artists', 
        'description': "Similar Artists",
        'cache_prefix': 'artist',
        }),
    url(ur'^music/(?P<artist>(?!/_/).*)/\+songs/$', views.artist_content, {
        'content_key': 'songs', 
        'description': "Songs",
        'cache_prefix': 'artist',
        }),
    url(ur'^music/(?P<artist>(?!/_/).*)/\+recommended/$', views.artist_content, {
        'content_key': 'song_playlist', 
        'description': "Recommended Songs",
        'cache_prefix': 'artist',
        }),
    url(ur'^music/(?P<artist>(?!/_/).*)/$', views.artist_home, {'cache_prefix': 'artist'}),


    # Ajax.
    url(r'^ajax/retrieval/$', views.retrieve_content),
    url(r'^ajax/clear/$', views.clear_resource),


    # Disallow web spiders.
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)


# HTTP 500 router.
handler500 = 'views.server_error'
