"""
template context format:
    page
    pending

    resource1.template_key: { resource1 subcontext dict }
    resource2.template_key: { resource2 subcontext dict }
    resource3.template_key: { resource3 subcontext dict }
    ...
"""
from __future__ import absolute_import
from itertools import chain
import json

from django.template import RequestContext
from django.shortcuts import render_to_response

from audiosearch.conf.display import ROWS_PER_TABLE as rows
from audiosearch.utils.decorators import stdout_gap
from audiosearch.utils.paginate import calculate_offset


# Polymorphic namespace for subcontext data tables
GENERIC_KEY = 'content'


def prepare(context, page):
    packaged = build_globals(page)

    for resource, datawrap in context.iteritems():
        # Subcontext key
        key = resource.template_key
        # Standard pairs
        base = build_base(resource)

        if datawrap:
            print 'hit'
            data, total_results = datawrap
            content = process_available(resource, data, total_results, page)
            packaged[key] = dict(chain(base.iteritems(), content.iteritems()))
        else:
            print 'miss'
            ajax_params = build_ajax(resource, page)
            packaged['pending'].append(ajax_params)
            packaged[key] = base

    return packaged


def prepare_async(request, resource_package, page):
    packaged = {}
    resource, datawrap = resource_package

    if datawrap:
        # Process normally
        data, total_results = datawrap
        base = build_base(resource, use_generic=True)
        context = process_available(resource, data, total_results, page)

        # Wrap context under the generic key and add globals
        context_wrap = build_globals(page)
        context_wrap[resource.template_key] = dict(chain(base.iteritems(), 
                                        context.iteritems()))

        # Render template section with context
        rendered = render_to_response(resource.template, context_wrap, 
                                    context_instance=RequestContext(request))
        
        # Set status and raw template html
        packaged['template'] = rendered.content
        packaged['status'] = 'complete'
    else:
        # No results
        # return no-results.html
        pass

    return packaged


def build_globals(page):
    """Template context global pairs."""
    return {
        'page': page,
        'pending': [],
    }

def build_base(resource, use_generic=False):
    """Pairs common to all subcontexts."""
    return {
        # 'template_key': GENERIC_KEY if use_generic else resource.template_key,
        'template_key': resource.template_key,
        'title': resource.description,
    }

def build_ajax(resource, page):
    """Params used in ajax loading."""
    querydict = resource.get_scheme()
    querydict['page'] = page
    return {
        'group': resource.group,
        'method': resource.method,
        'querydict': json.dumps(querydict),
        'template_key': resource.template_key,
    }

def process_available(resource, data, total_results, page):
    total_pages = total_results / rows
    index = calculate_offset(page, total_pages, total_results)

    # Page nav; use initial page if page exceeds total pages
    current = page if page <= total_pages else 1
    next_ = current + 1 if (current * rows) < total_results else 0
    previous = current - 1 if current <= total_pages else total_pages

    return {
        'current': current,
        'echodata': data,
        'index': index,
        'next': next_,
        'previous': previous,
        'row_count': rows,
        'total_pages': total_pages,
        'total_results': total_results,
        'complete': True,
    }
