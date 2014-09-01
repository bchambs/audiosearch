from __future__ import absolute_import

from audiosearch.services.base import EchoNestService


# TODO: create scheduled service to update this.
class TopArtistsService(EchoNestService):
    TYPE_ = 'artist'
    METHOD = 'top_hottt'
    BUCKETS = [
        'hotttnesss_rank',
    ]
    ECHO_NEST_KEY = 'artists'


    def __init__(self):
        payload = {
            'results': EchoNestService._PERSIST,
            'bucket': TopArtistsService.BUCKETS,
        }
        super(TopArtistsService, self).__init__(self.TYPE_, self.METHOD, payload)

    def __str__(self):
        return "TopArtistsService"
