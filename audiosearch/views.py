"""
Regular view (not async) execution:
    1. Establish args/kwargs and redirect if necessary.
    2. Create requested resources.
    3. Assign resources to 'available' or 'pending' status lists.
    4. Pass TemplateResponse to context mapper middleware.
"""

from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, RequestContext
from django.template.response import TemplateResponse

from audiosearch import Cache
from audiosearch.conf import DEFAULT_ROW_COUNT, HOME_ROW_COUNT
from audiosearch.models import make_key, resource 
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


# TODO: fix the need for this, 'content['is_pending'] = True'
# Add titles to resource classes
# Move '14' to constant
@stdout_gap
def music_home(request, GET, **params):

    context = {
        'available': [],
        'pending': [],
        'row_count': HOME_ROW_COUNT,
    }

    row_count = HOME_ROW_COUNT
    top = resource.TopArtists()

    if top.key in Cache:
        resource_data = Cache.get_list(top.key, 0, 14)
        context['available'].append(top.res_id, resource_data)
    else:
        top.get_resource()
        context['pending'].append(top)

    return TemplateResponse(request, 'music-home.html', context)


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
    row_count = GET.get('row_count', DEFAULT_ROW_COUNT)

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


# TODO: move this somewhere
def _calculate_page_range(page, count):
    count = int(count)

    if page:
        start = int(page) * count
        end = start + count
    else:
        start = 0
        end = count - 1

    return start, end


