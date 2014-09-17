from __future__ import absolute_import
import json

from django.http import HttpResponse
from django.shortcuts import redirect, render, render_to_response
from django.template import Context, RequestContext

from audiosearch import Cache
from audiosearch.conf import NROWS_DEFAULT
from audiosearch.core import handlers
from audiosearch.models import resource
from audiosearch.utils.decorators import reset_cache, stdout_gap


# @reset_cache('top')
@stdout_gap
def music_home(request, GET, **params):
    context = {}
    top = resource.TopArtists()
    # try:
    #     raw_data = Cache.get(top.key, top.dispatch())
    # except FailedKeyError:
    #     process_failed(top)

    # status = Cache.get_status(top.key)
    # top_content = handlers.dispatch(top, status)
    # context[top.resource_id] = top_content

    return render(request, 'music-home.html', context)

    # if status == 'available':
    #     raw_data, size = Cache.get_list_bundle(top.key, 0, 14)
    #     content_map = Available.process(top, raw_data, size, 0, 14)
    # elif status == 'failed':
    #     content_map = Failed.process(top)
    # else:
    #     top.get_resource()
    #     content_map = Pending.process(top)

    # context[top.res_id] = content_map

    # print context[top.res_id]

    # return render(request, 'music-home.html', context)


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
    key = resource.make_key(group, category, name)

    if key in Cache:
        # Build dict to load table in content_rows.html
        content = {}
        start, end = _calculate_page_range(page, row_count)
        content['offset'] = start - 1
        content['resource_data'], content['total_data'] = Cache.get(key, start, end)

        # Render template html then send with status as JSON encoded bundle.
        template_html = render_to_response('content_rows.html', content, 
                                context_instance=RequestContext(request))
        context['template'] = template_html.content
        context['status'] = 'complete'
    else:
        context['status'] = 'pending'
    
    return HttpResponse(json.dumps(context), content_type="application/json")

