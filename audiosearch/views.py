from __future__ import absolute_import
from collections import namedtuple
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch import Cache
from audiosearch.handlers import miss
from audiosearch.models import resource 
from audiosearch.utils.decorators import stdout_gap


# Resource = namedtuple('Resource', 'id_ key')


# def make_key(category, content, name):
#     id_ = ' '.join([category, content])
#     key = '::'.join([id_, name])
#     return Resource(content, key)


@stdout_gap
def artist_home(request, GET, **params):
    try:
        artist = params.pop('artist')
    except KeyError:
        return redirect(music_home)

    content = {}
    pending = []
    profile = make_key('artist', 'profile', artist)
    disc = make_key('artist', 'discography', artist)

    profile_data = Cache.get_hash(profile.key)
    if profile_data:
        content[profile.id_] = profile_data
    else:
        pending.append(profile.key)

    disc_data = Cache.get_list(disc.key, 0, 14)
    if disc_data:
        content[disc.id_] = disc_data
    else:
        pending.append(profile.key)

    content['pending'] = pending
    context = Context(content)

    return render(request, 'artist-home.html', context)


@stdout_gap
def music_home(request, GET, **params):
    content = {}
    top = resource.TopArtists()

    if top.key in Cache:
        content[top.rid] = Cache.get_list(top.key, 0, 14)
    else:
        content['pendingA'] = top.rid
        # top.get()

    # prof = resource.ArtistProfile('bright eyes')
    # prof.get()
    # print

    prof2 = resource.SongProfile('bright eyes', 'something vague')
    prof2.get()


    context = Context(content)
    return render(request, 'music-home.html', context)

