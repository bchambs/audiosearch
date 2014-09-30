from __future__ import absolute_import
import json

from django.http import HttpResponse

from audiosearch import models


class AsyncClassLoader(object):
    """Construct resource instance from ajax params."""
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.is_ajax():
            return

        try:
            # Module name
            group = view_kwargs.pop('group')
            # Class name
            method = view_kwargs.pop('method')
            # Map scheme to cls._fields to generate init arg list
            scheme = view_kwargs.pop('scheme')

            # Get class string from module then execute cls alt constructor
            resource_module = vars(models).get(group)
            klass = getattr(resource_module, method.title())
            resource = klass.from_dict(**scheme)
        except (AttributeError, KeyError, TypeError) as e:
            # Invalid ajax param(s); request will never succeed
            print e
            return HttpResponse(json.dumps({'status': 'failed'}),
                                content_type="application/json")
        
        # Pass resource instance to view kwargs
        view_kwargs['resource'] = resource
