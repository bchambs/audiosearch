import logging

import audiosearch.config as cfg
from audiosearch.settings import DEBUG as DJANGO_DEBUG
from audiosearch.redis import client as RC

log = logging.getLogger(__name__)

class AudiosearchDebug(object):
    def process_request(self, request):
        """
        If project is in debug mode, use query params to enable debugging.
        """

        if DJANGO_DEBUG:
            query_params = request.GET.dict()
            debug_params = query_params.get('debug')
            resource_id = query_params.get('q')

            if debug_params:
                debug_params = debug_params.lower()
                opts = ""

                if 'v' in debug_params:
                    cfg.VIEW_DEBUG = True
                    opts += "view "
                else: 
                    cfg.VIEW_DEBUG = False

                if 'c' in debug_params:
                    cfg.CONSUMER_DEBUG = True
                    opts += "consumer "
                else: 
                    cfg.CONSUMER_DEBUG = False

                if 'r' in debug_params:
                    cfg.REDIS_DEBUG = True
                    opts += "redis "
                else: 
                    cfg.REDIS_DEBUG = False

                if len(opts) > 0:
                    log.info(opts)

            else:
                cfg.VIEW_DEBUG = False
                cfg.CONSUMER_DEBUG = False
                cfg.REDIS_DEBUG = False

            ###############################

            if cfg.REDIS_DEBUG:
                RC.delete(resource_id)

        return None


