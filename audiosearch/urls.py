from django.conf.urls import patterns, include, url
from django.http import HttpResponse

from src import views


urlpatterns = patterns('',
    url(ur'^$', views.index), 


    url(ur'^search/$', views.search),
    url(ur'^music/$', views.top_artists),


    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/\+similar/$', views.song_content, {'content_key': 'song_playlist', 'description': "Similar Songs"}),
    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/\+recommended/$', views.song_content, {'content_key': 'similar_artists', 'description': "Recommended Artists"}),
    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/$', views.song_home),


    url(ur'^music/(?P<artist>(?!/_/).*)/\+similar/$', views.artist_content, {'content_key': 'similar_artists', 'description': "Similar Artists"}),
    url(ur'^music/(?P<artist>(?!/_/).*)/\+songs/$', views.artist_content, {'content_key': 'songs', 'description': "Songs"}),
    url(ur'^music/(?P<artist>(?!/_/).*)/\+recommended/$', views.artist_content, {'content_key': 'song_playlist', 'description': "Recommended Songs"}),
    url(ur'^music/(?P<artist>(?!/_/).*)/$', views.artist_home),
    

    # url(ur'^music/(?P<artist>[^/]+)/$', views.artist_summary),
    # url(ur'^music/(?P<artist>[^/]+)/similar/$', views.artist_content, {'content_key': 'similar_artists', 'description': "Similar Artists"}),
    # url(ur'^music/(?P<artist>[^/]+)/songs/$', views.artist_content, {'content_key': 'songs', 'description': "Songs"}),
    # url(ur'^music/(?P<artist>[^/]+)/recommended/$', views.artist_content, {'content_key': 'song_playlist', 'description': "Recommended Songs"}),


    # url(ur'^music/(?P<artist>[^/]+)/(?P<song>[^/]+)/$', views.song_summary),
    # url(ur'^music/(?P<artist>[^/]+)/(?P<song>[^/]+)/similar/$', views.song_content, {'content_key': 'song_playlist', 'description': "Similar Songs"}),
    # url(ur'^music/(?P<artist>[^/]+)/(?P<song>[^/]+)/recommended/$', views.song_content, {'content_key': 'similar_artists', 'description': "Recommended Artists"}),


    url(r'^ajax/retrieval/$', views.retrieve_content),
    url(r'^ajax/clear/$', views.clear_resource),
    url(r'^ajax/debug_template/$', 'src.views.debug_template'),


    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)



handler500 = 'views.server_error'
