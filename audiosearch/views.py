from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch import Cache
# from audiosearch.redis import KeyNotFoundError
from audiosearch.handlers import miss
from audiosearch.models import resource 


def artist_home(request, GET, **params):
    print
    print
    try:
        artist = params.pop('artist')
    except KeyError:
        return redirect(music_home)

    profile = resource.ArtistProfile(artist)
    disc = resource.Discography(artist)

    p2 = resource.ArtistProfile(artist)

    resources = [
        profile,
        disc,
        p2,
    ]


    available, failed, pending = Cache.get_many(resources)


    # for _ in resources:
    #     print
    #     print _.id
    #     print _.key
    #     print _.ttl
    #     print

    """
    'artist name' : {
        'artist profile': {
            __pageinfo__,
            ...
        }
    }

    """
    context = Context({
        'test': 1,
    })


    print
    print
    return render(request, 'artist-home.html', context)









def music_home(request, GET, opt):
    context = Context({})
    return render(request, 'music-home.html', context)




