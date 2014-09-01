from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.http import HttpResponse

from audiosearch import views


urlpatterns = patterns('',

    # General.
    # url(ur'^$', views.index), 
    # url(ur'^about/$', views.about),
    # url(ur'^search/$', views.search),
    url(ur'^music/$', views.music_home),
    # url(ur'^trending/$', views.trending),


    # Songs.
    # url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/\+similar/$', views.song_content, {'content_key': 'song_playlist'}),
    # url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/\+recommended/$', views.song_content, {'content_key': 'similar_artists'}),
    # url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/$', views.song_home),


    # Artists.
    # url(ur'^music/(?P<artist>(?!/_/).*)/\+similar/$', views.artist_content, {'content_key': 'similar_artists'}),
    # url(ur'^music/(?P<artist>(?!/_/).*)/\+songs/$', views.artist_content, {'content_key': 'songs'}),
    # url(ur'^music/(?P<artist>(?!/_/).*)/\+recommended/$', views.artist_content, {'content_key': 'song_playlist'}),
    url(ur'^music/(?P<artist>(?!/_/).*)/$', views.artist_home),


    # Ajax.
    # url(ur'^ajax/retrieval/$', views.retrieve_content),
    # url(ur'^ajax/clear/$', views.clear_resource),


    # Disallow web spiders.
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)


# HTTP 500 router.
# handler500 = 'views.server_error'
