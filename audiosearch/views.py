from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, RequestContext

from audiosearch import Cache
from audiosearch.conf import N_ROWS_PTABLE, N_ROWS_HTABLE
from audiosearch.models import make_key, resource 
from audiosearch.utils.decorators import stdout_gap


@stdout_gap
def artist_home(request, GET, **params):
    print 'why are you here_________________' * 5
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
        'div_id': top.rid,
        'row_count': row_count,
        'title': "Popular artists",
    }
    pending = []

    if top.key in Cache:
        # content['resource_data'] = Cache.get_list(top.key, 0, 14)
        pass
    else:
        # opts = _create_opts(top, row_count=row_count)
        # content['pending'] = [opts]
        # content['is_pending'] = True
        # top.get_resource()
        pass

    ####################### testing
    top.get_resource()
    content['is_pending'] = True
    opts = _create_opts(top, row_count=row_count)
    pending.append(opts)
    ####################### testing

    namespaced = {
        top.rid: content,
        'pending': pending,
    }

    return render(request, 'music-home.html', Context(namespaced))


def ajax_retrieve_content(request, GET, **params):
    try:
        group = params.pop('group')
        category = params.pop('category')
        name = params.pop('name')
    except KeyError:
        return HttpResponse(json.dumps({'status': 'failed'}), 
                            content_type="application/json")
    
    context = {}
    page = GET.get('page')
    row_count = GET.get('row_count', N_ROWS_PTABLE)

    key = make_key(group, category, name)

    if key in Cache:    # Build dict to load table in content_rows.html
        content = {}
        start, end = _calculate_page_range(page, row_count)
        content['offset'] = start - 1
        content['resource_data'] = Cache.get(key, start, end)

        # Render template html then send with status as JSON encoded bundle.
        template_html = render_to_response('content_rows.html', content, 
                                context_instance=RequestContext(request))

        context['template'] = template_html.content
        context['status'] = 'complete'
    else:
        context['status'] = 'pending'
    
    return HttpResponse(json.dumps(context), content_type="application/json")


def _create_opts(resource, page=None, row_count=None):
    opts = {
        'group': resource.group,
        'category': resource.category,
        'div_id': resource.rid,
        'name': resource.name,
        'qstring': {},
    }

    if page: 
        opts['qstring']['page'] = page

    if row_count: 
        opts['qstring']['row_count'] = row_count

    return opts


def _calculate_page_range(page, count):
    count = int(count)

    if page:
        start = int(page) * count
        end = start + count
    else:
        start = 0
        end = count - 1

    return start, end


