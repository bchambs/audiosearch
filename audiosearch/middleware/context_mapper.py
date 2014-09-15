from __future__ import absolute_import

from django.template.response import TemplateResponse

from audiosearch.utils.decorators import stdout_gap


class ResourceContextMapper(object):

    @stdout_gap
    def process_template_response(self, request, response):
        available = response.context_data.get('available')
        page = response.context_data.get('page')
        pending = response.context_data.get('pending')
        row_count = response.context_data.get('row_count')
        template = response.template_name
        processed = {
            'pending': [],
        }

        for resource, data, total in available:
            processed[resource.res_id] = {
                'resource_data': data,
                'total_data': total,
                'title': resource.title,
            }

        for resource in pending:
            processed[resource.res_id] = {
                'div_id': resource.res_id,
                'title': resource.title,
            }
            opts = create_opts(resource, page, row_count)
            processed['pending'].append(opts)

        return TemplateResponse(request, template, processed)


def create_opts(resource, page, row_count):
    opts = {
        'group': resource.group,
        'category': resource.category,
        'div_id': resource.res_id,
        'name': resource.name,
        'qstring': {},
    }

    if page: 
        opts['qstring']['page'] = page
    if row_count: 
        opts['qstring']['row_count'] = row_count

    return opts

