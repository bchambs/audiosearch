from audiosearch.settings import DEBUG as DJANGO_DEBUG


class AudiosearchDebug(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if DJANGO_DEBUG and not request.is_ajax():
            view_kwargs['debug'] = True

        return None
