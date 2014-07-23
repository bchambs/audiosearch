import audiosearch.config as cfg
from audiosearch.settings import DEBUG as DJANGO_DEBUG

class AudiosearchDebug(object):
    def process_request(self, request):
        """
        If project is in debug mode, use query params to enable debugging.
        """
        if DJANGO_DEBUG:
            if 'debug' in request.GET:
                opts = request.GET['debug'].lower()

                cfg.REDIS_DEBUG = True if 'r' in opts else False
                cfg.VIEW_DEBUG = True if 'v' in opts else False
                cfg.CONSUMER_DEBUG = True if 'c' in opts else False

                if len(opts) > 0:
                    print
                    print "DEBUG: ", 
                    if cfg.REDIS_DEBUG: print "REDIS ",
                    if cfg.VIEW_DEBUG: print "VIEW ",
                    if cfg.CONSUMER_DEBUG: print "CONSUMER ",
                    print
                    print
            else:
                cfg.REDIS_DEBUG = False
                cfg.VIEW_DEBUG = False
                cfg.CONSUMER_DEBUG = False

        return None


