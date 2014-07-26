from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.contrib import admin

from src import views

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'src.views.index'), 

    url(r'^music/(?P<artist>[\w|\W]+)/similar/$', views.similar, {'type': "artist"}),
    url(r'^music/(?P<artist>[\w|\W]+)/$', views.artist),

    url(r'^ajax/clear/$', 'src.views.clear_resource'),
    url(r'^ajax/debug_template/$', 'src.views.debug_template'),

    (r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
)

handler500 = 'src.views.server_error'
