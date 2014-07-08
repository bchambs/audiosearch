from random import choice, sample

from src.util import get_good_bio, debug, debug_subtitle, remove_duplicate_songs


class ENCall(object):
    """
    Abstract class representing input to request.get().
    """

    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"

    def __init__(self, type_, method, id_, buckets):
        self.url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self.id_ = id_
        self.payload = {
            'api_key': "QZQG43T7640VIF4FN",
            'format': "json",
            'bucket': buckets,
        }

    def trim(self, data):
        return data


class ArtistProfile(ENCall):
    """
    Package representing all required data for an artist profile request from Echo Nest.
    """

    # REST data
    TYPE_ = "artist"
    METHOD = "profile"
    BUCKETS = [
        'biographies',
        'hotttnesss',
        'images',
        'terms',
        'hotttnesss_rank',
    ]

    # REDIS data
    KEY_ = 'artist'
    REDIS_ID = 'profile'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_


    def trim(self, data):
        result = {
            'name': data['name'],
            'hotttnesss_rank': data['hotttnesss_rank'],
        }

        if 'biographies' in data:
            result['bio_full'] = get_good_bio(data['biographies'])

            # summary: get first paragraph, if not optimal take first 500 letters
            paragraphs = result['bio_full'].split("\n")

            if len(paragraphs[0]) < 200 or len(paragraphs[0]) > 500:
                result['bio_trunc'] = result['bio_full'][:500]
            else:
                result['bio_trunc'] = paragraphs[0]

            # TODO: remove this
            del result['bio_full']

        # banner images, take top 4 images, create (id, url) tuple, append to tiles key
        if 'images' in data:
            result['tiles'] = []
            temp = sample(data['images'], 4)

            for x in range(0, len(temp)):
                tup = 'tile-image-' + str(x + 1), temp[x]['url']
                result['tiles'].append(tup)

        if 'terms' in data:
            try:
                if len(data['terms']) is 1:
                    result['terms'] = data['terms'][0]['name']
                else:
                    result['terms'] = data['terms'][0]['name'] + ', ' + data['terms'][1]['name']
            
            # CATCH handle the unlikely event that a term item exists without a name key
            except KeyError:
                pass

        if 'hotttnesss' in data:
            result['hotttnesss'] = int(round(data['hotttnesss'] * 100))

        return result


class Playlist(ENCall):
    """
    Package representing all required data for a playlist request from Echo Nest.
    """

    # REST data
    TYPE_ = "playlist"
    METHOD = "static"
    BUCKETS = [
        'song_hotttnesss',
    ]

    # REDIS data
    KEY_ = 'songs'
    REDIS_ID = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['artist_id'] = id_
        self.payload['results'] = 100
        self.payload['sort'] = "song_hotttnesss-desc"

    def trim(self, data):
        for song in data:
            song['song_hotttnesss'] = int(round(song['song_hotttnesss'] * 100))
        return data


class SimilarArtists(ENCall):
    """
    Package representing all required data for a similar artists request from Echo Nest.
    """

    # REST data
    TYPE_ = "artist"
    METHOD = "similar"
    BUCKETS = [
        'images',
        'terms',
        'familiarity',
        'songs',
    ]

    # REDIS data
    KEY_ = 'artists'
    REDIS_ID = 'similar'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_
        self.payload['results'] = 100


    def trim(self, data):
        for artist in data:
            artist['familiarity'] = int(round(artist['familiarity'] * 100))
            if 'images' in artist:
                artist['preview_url'] = artist['images'][0]['url']

            if 'terms' in artist:
                try:
                    if len(artist['terms']) is 1:
                        artist['terms'] = artist['terms'][0]['name']
                    else:
                        artist['terms'] = artist['terms'][0]['name'] + ', ' + artist['terms'][1]['name']
                
                # CATCH handle the unlikely event that a term item exists without a name key
                except KeyError:
                    pass

            if 'songs' in artist:
                artist['songs'] = remove_duplicate_songs(artist['songs'], 3)

            del artist['images']

            
        return data[:5]


