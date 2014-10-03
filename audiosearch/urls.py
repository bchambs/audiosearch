from __future__ import absolute_import

from django.conf.urls import patterns, url
from django.http import HttpResponse

from audiosearch import views


urlpatterns = patterns('',

    # General
    url(ur'^search/$', views.search, name='search'),
    url(ur'^music/$', views.music_home),

    # Songs
    url(ur'^music/(?P<artist>(?!/_/).*)/_/(?P<song>.*)/$', views.song_home, name='song_home'),

    # Artists
    url(ur'^music/(?P<artist>(?!/_/).*)/$', views.artist_home, name='artist_home'),

    # Ajax
    url(ur'^ajax/(?P<group>.+)/(?P<method>.+)/$', views.ajax_retrieve, name='ajax_retrieve'),
    url(ur'^ajax/clear/$', views.ajax_clear, name='ajax_clear'),

    # Disallow web spiders
    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)


# HTTP 500 router
# handler500 = 'views.server_error'

