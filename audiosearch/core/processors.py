"""Keywords for content-dicts in templates
generic key='content'

global:
    page
    pending

available:
    echodata
    next
    previous
    row_count
    template_id
    title
    total_results

pending:
    alias
    group
    method
    template_id
    title

ajax wrapped in generic dict:
    
"""

from __future__ import absolute_import
from itertools import chain

from django.template import RequestContext
from django.shortcuts import render_to_response

from audiosearch.conf.display import ROWS_PER_TABLE as rows


def prepare(context, page):
    # Content wrapper; all pairs are globally visible in templates
    packaged = {
        'page': page,
        'pending': [],
    }

    for resource, datapack in context.iteritems():
        # Template key
        key = resource.method
        # Standard mapping
        base = build_base(key, resource.description)

        if datapack:
            content = process_available(resource, datapack, page)
        else:
            content = process_pending(resource)
            packaged['pending'].append(resource)

        packaged[key] = dict(chain(base.iteritems(), content.iteritems()))

    return packaged


def prepare_async(request, data_pair, page):
    packaged = {}
    wrap = {}
    key = 'content'
    resource, datapack = data_pair

    if datapack:
        base = build_base(key, resource.description)
        context = process_available(resource, datapack, page)
        # Map resource context to generic template key
        wrap[key] = dict(chain(base.iteritems(), context.iteritems()))
        # Render template section with context
        template = render_to_response('content_rows.html', wrap, 
                                        context_instance=RequestContext(request))
        # Add template's html
        packaged['template'] = template.content
        packaged['status'] = 'complete'
    else:
        packaged['status'] = 'pending'

    return packaged


def build_base(key, title):
    return {
        'template_id': key,
        'title': title
    }

def process_available(resource, datapack, page):
    data, total_cached = datapack

    return {
        'echodata': data,
        'row_count': rows,
        'total_results': total_cached,
        'next': page + 1 if (page * rows) < total_cached else 0,
        'previous': page - 1 if page > 1 else 0,
    }

def process_pending(resource):
    """Ajax opts."""
    return {
        'group': resource.group,
        'method': resource.method,
        'alias': resource.alias,
    }
