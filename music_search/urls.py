from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'home.views.index'),   
    url(r'^search/$', 'home.views.search'),
    url(r'^artist/$', 'home.views.artist_info'),
    url(r'^song/$', 'home.views.song_info'),
    #url(r'^admin/', include(admin.site.urls)),
)
