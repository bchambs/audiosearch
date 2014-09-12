from __future__ import absolute_import
import ast
import json

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context

from audiosearch import Cache
from audiosearch.conf import N_ROWS_PTABLE, N_ROWS_HTABLE
from audiosearch.models import make_id, make_key, resource 
from audiosearch.utils.decorators import stdout_gap


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
    row_count = N_ROWS_HTABLE
    top = resource.TopArtists()
    content = {
        'title': "Popular artists",
        'row_count': row_count,
    }

    if top.key in Cache:
        resource_data = Cache.get_list(top.key, 0, 14)
        content[top.rid] = dict(resource_data=resource_data)
    else:
        opts = _create_opts(top, row_count)
        content['pending'] = [opts]
        top.get_resource()

    opts = _create_opts(top, row_count)
    content['pending'] = [opts]

    context = Context(content)
    return render(request, 'music-home.html', context)


def ajax_retrieve_content(request, GET, **params):
    context = {}
    category = GET.get('category')
    content = GET.get('content')
    name = GET.get('name')
    page = GET.get('page')
    row_count = GET.get('row_count', N_ROWS_PTABLE)

    if not category or not content or not name:
        return HttpResponse(json.dumps({'status': 'failed'}), 
                            content_type="application/json")

    key = make_key(category, content, name)

    if key in Cache:
        start, end = _calculate_page_range(page, row_count)
        context['resource_data'] = Cache.get(key, start, end)
        context['resource_type'] = content
        context['div_id'] = make_id(category, content)
        context['status'] = 'complete'
    else:
        context['status'] = 'pending'

    return HttpResponse(json.dumps(context), content_type="application/json")


def _create_opts(resource, row_count, page=None):
    params = {
        'category': resource.category,
        'content': resource.content,
        'name': resource.name,
        'row_count': row_count,
    }

    if page: 
        params['page'] = page

    return json.dumps(params, ensure_ascii=False)


def _calculate_page_range(page, count):
    if page:
        start = page * count
        end = start + count
    else:
        start = 0
        end = count
    return start, end
