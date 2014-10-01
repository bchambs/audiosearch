from __future__ import absolute_import

from audiosearch.utils.sanitizers import normalize


class Normalizer(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        normal_GET = {}
        normal_kwargs = {}

        if request.GET:
            normal_GET = normalize(request.GET.copy())

        if view_kwargs:
            normal_kwargs = normalize(view_kwargs)

        page = int(normal_GET.get('page', 1))
        page = 1 if page < 1 else page

        return view_func(request, normal_GET, page, **normal_kwargs)
