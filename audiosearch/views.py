from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch import Cache
# from audiosearch.redis import KeyNotFoundError
from audiosearch.handlers import miss
from audiosearch.models import resource 
from audiosearch.utils.decorators import debug_view


@debug_view
def artist_home(request, GET, opt):

    x = Cache.get('test')
    print x

    context = Context({})
    return render(request, 'artist-home.html', context)


    ###################
    try:
        artist = opt.pop('artist')
    except KeyError:
        return redirect(music_home)

    profile = resource.ArtistProfile(artist)
    disc = resource.Discography(artist)

    content = _get_content(profile, disc)


    # for _ in resources:
    #     print
    #     print _.id
    #     print _.key
    #     print _.ttl
    #     print


    context = Context({})
    return render(request, 'artist-home.html', context)


def _get_content(*resources):
    available = dict()

    for res in resources:
        try:
            available[res.key] = cache.fetch(res.key, res.ttl)
        except cache.KeyNotFoundError:
            pass

    return available






def music_home(request, GET, opt):
    context = Context({})
    return render(request, 'music-home.html', context)




