from django.conf.urls import patterns, include, url

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
    #url(r'^admin/', include(admin.site.urls)),
)
