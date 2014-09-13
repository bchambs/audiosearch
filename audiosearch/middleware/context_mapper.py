from __future__ import absolute_import

from django.template.response import TemplateResponse

from audiosearch.utils.decorators import stdout_gap
from audiosearch.utils.print_formats import fprint_dict


class ResourceContextMapper(object):

    @stdout_gap
    def process_template_response(self, request, response):
        available = response.context_data.get('available')
        pending = response.context_data.get('pending')
        page = response.context_data.get('page')
        row_count = response.context_data.get('row_count')
        template = response.template_name

        processed = dict(available, pending=[]) # TODO: list literal may be bad

        for resource in pending:
            opts = create_opts(resource, page, row_count)
            processed['pending'].append(opts)

        #####
        if 'available' in processed:
            fprint_dict("Available, mw context", processed['available'])

        for optsd in processed['pending']:
            fprint_dict("Pending, mw context", optsd)
        #####
        
        return TemplateResponse(request, template, processed)


def create_opts(resource, page, row_count):
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

