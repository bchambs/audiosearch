import time

__all__ = ['Request']

# encapsulate this in case I change what I want displayed
class Request:
    def __init__(self, artist, song=None):
        self._request = {'_artist': artist}

        # if song:
        #     self._request = {
        #         '_artist': None
        #         '_artid': artist
        #         '_song': None
        #     }
        # else:
        #     self._request = {
        #         '_artist': artist
        #     }

    def serve(self):
        snooze = 2

        while not self._request:
            try:
                _request['_artist'] = artist.Artist(_request['_artid'], limit=True, buckets=['biographies', 'hotttnesss', 'images', 'terms'])

            except EchoNestAPIError:
                time.sleep(snooze)
    # def serve(self):
    #     snooze = 2

    #     while not self._ready:
    #         try:
    #             _request['_artist'] = artist.Artist(_request['_artid'], limit=True, buckets=['biographies', 'hotttnesss', 'images', 'terms'])

    #             if '_song' in _request:
    #                 try:
    #                     _request['_song'] = song.search(artist_id=_request['_artid'], sort='song_hotttnesss-desc', results=35)

    #                 except EchoNestAPIError:
    #                     time.sleep(snooze)

    #             self._ready = True

    #         except EchoNestAPIError:
    #             time.sleep(snooze)

