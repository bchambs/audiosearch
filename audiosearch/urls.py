from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib import admin

from src import views

admin.autodiscover()

urlpatterns = patterns('',
    url(ur'^$', views.index), 


    url(ur'^search/$', views.search),


    url(ur'^music/(?P<artist>[^/]*)/$', views.artist),
    url(ur'^music/(?P<artist>[^/]*)/similar/$', views.similar),
    url(ur'^music/(?P<artist>[^/]*)/songs/$', views.artist_songs),


    url(ur'^music/(?P<artist>[^/]*)/(?P<song>[^/]*)/$', views.song),
    url(ur'^music/(?P<artist>[^/]*)/(?P<song>[^/]*)/similar/$', views.similar),


    url(r'^ajax/retrieval/$', views.retrieve_content),
    url(r'^ajax/clear/$', views.clear_resource),
    url(r'^ajax/debug_template/$', 'src.views.debug_template'),


    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler500 = 'views.server_error'
