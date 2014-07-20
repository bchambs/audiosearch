from __future__ import absolute_import

from random import choice, sample
import datetime

# from src.util import get_good_bio, debug, debug_subtitle, remove_duplicate_songs
import src.util as util


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
        }
        if buckets:
            self.payload['bucket'] = buckets

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
        result = {}

        if 'name' in data:
            result['name'] = data['name']

        if 'images' in data:
            result['title_image'] = data['images'][0]['url']

        if 'terms' in data:
            result['terms'] = []

            for x in range(0,5):
                try:
                    result['terms'].append(data['terms'][x]['name'])
                except IndexError:
                    break

        return result

        # result = {}
        # if 'name' in data:
        #     result['name'] = data['name']

        # if 'hotttnesss_rank' in data:
        #     result['hotttnesss_rank'] = data['hotttnesss_rank']

        # if 'biographies' in data:
        #     result['bio_full'] = util.get_good_bio(data['biographies'])

        #     # summary: get first paragraph, if not optimal take first 500 letters
        #     paragraphs = result['bio_full'].split("\n")

        #     if len(paragraphs[0]) < 200 or len(paragraphs[0]) > 500:
        #         result['bio_trunc'] = result['bio_full'][:500]
        #     else:
        #         result['bio_trunc'] = paragraphs[0]

        #     # TODO: remove this
        #     del result['bio_full']

        # # banner images, take top 4 images, create (id, url) tuple, append to tiles key
        # if 'images' in data:
        #     result['tiles'] = []
        #     temp = []

        #     if len(data['images']) > 4:
        #         temp = sample(data['images'], 4)
        #     else: 
        #         temp = data['images']

        #     for x in range(0, len(temp)):
        #         tup = 'tile-image-' + str(x + 1), temp[x]['url']
        #         result['tiles'].append(tup)

        # if 'terms' in data:
        #     if len(data['terms']) > 0:
        #         try:
        #             if len(data['terms']) is 1:
        #                 result['terms'] = data['terms'][0]['name']
        #             else:
        #                 result['terms'] = data['terms'][0]['name'] + ', ' + data['terms'][1]['name']
                
        #         # CATCH handle the unlikely event that a term item exists without a name key
        #         except KeyError:
        #             pass

        # if 'hotttnesss' in data:
        #     result['hotttnesss'] = int(round(data['hotttnesss'] * 100))

        # return result


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
        result = []

        result = data

        return data

        # result = {}
        # terms = {}

        # for i in range(0,20):
        #     sim = data[i]
        #     for t in range(0,5):
        #         try:
        #             term = sim['terms'][t]['name']
        #             terms[term] = terms.get(term, 0) + 1
        #         except IndexError:
        #             break

        # result['terms'] = terms

        # for k, v in terms.items():
        #     print "%s: %s" % (k, v)

        # return result



        # for artist in data:
        #     artist['familiarity'] = int(round(artist['familiarity'] * 100))
        #     if 'images' in artist:
        #         artist['preview_url'] = artist['images'][0]['url']

        #     if 'terms' in artist:
        #         if len(artist['terms']) > 0:
        #             try:
        #                 if len(artist['terms']) is 1:
        #                     artist['terms'] = artist['terms'][0]['name']
        #                 else:
        #                     artist['terms'] = artist['terms'][0]['name'] + ', ' + artist['terms'][1]['name']
                
        #             # CATCH handle the unlikely event that a term item exists without a name key
        #             except KeyError:
        #                 pass

        #     if 'songs' in artist:
        #         artist['songs'] = util.remove_duplicate_songs(artist['songs'], 3)

        #     del artist['images']

        # return data


class ArtistSearch(ENCall):
    """
    Package representing all required data for an artist search request from Echo Nest.
    """

    # REST data
    TYPE_ = "artist"
    METHOD = "suggest"

    # REDIS data
    KEY_ = 'artists'
    REDIS_ID = 'artists'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, None)
        self.payload['name'] = id_
        self.payload['results'] = 100


    def trim(self, data):
        return data


class SongSearch(ENCall):
    """
    Package representing all required data for an song search request from Echo Nest.
    """

    # REST data
    TYPE_ = "song"
    METHOD = "search"

    # REDIS data
    KEY_ = 'songs'
    REDIS_ID = 'songs'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, None)
        self.payload['title'] = id_
        self.payload['results'] = 100
        self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['song_type'] = "studio"


    def trim(self, data):
        return data


class SimilarSongs(SongSearch):
    """
    Package representing all required data for an similar songs request from Echo Nest.
    """


    REDIS_ID = 'similar_songs' 


    def __init__(self, id_, base, offset):
        SongSearch.__init__(self, id_)
        # self.payload['sort'] = "song_hotttnesss-desc"
        self.payload['sort'] = "artist_familiarity-desc"
        self.payload['limit'] = True
        self.payload['bucket'] = 'id:7digital-US'

        offset = .1
        styles = ['indie rock', 'indie', 'folk', 'emo', 'rock']
        self.payload['style'] = styles

        del(self.payload['title'])

        if 'tempo' in base:
            self.payload['max_tempo'] = util.calculate_offset(base['tempo'], offset * 1000, 500) # TODO: move limits to a constants file
            self.payload['min_tempo'] = util.calculate_offset(base['tempo'], offset * 1000, 0)

        if 'loudness' in base:
            self.payload['max_loudness'] = util.calculate_offset(base['loudness'], offset * 100, 100)
            self.payload['min_loudness'] = util.calculate_offset(base['loudness'], offset * 100, -100)

        if 'danceability' in base:
            self.payload['max_danceability'] = util.calculate_offset(base['danceability'], offset, 1)
            self.payload['min_danceability'] = util.calculate_offset(base['danceability'], offset, 0)

        if 'energy' in base:
            self.payload['max_energy'] = util.calculate_offset(base['energy'], offset, 1)
            self.payload['min_energy'] = util.calculate_offset(base['energy'], offset, 0)

        if 'liveness' in base:
            self.payload['max_liveness'] = util.calculate_offset(base['liveness'], offset, 1)
            self.payload['min_liveness'] = util.calculate_offset(base['liveness'], offset, 0)

        if 'max_speechiness' in base:
            self.payload['max_max_speechiness'] = util.calculate_offset(base['max_speechiness'], offset, 1)
            self.payload['min_max_speechiness'] = util.calculate_offset(base['max_speechiness'], offset, 0)


    def trim(self, data):
        return data


class SongProfile(ENCall):
    """
    Package representing all required data for an song profile request from Echo Nest.
    """

    # REST data
    TYPE_ = "song"
    METHOD = "profile"
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        # 'tracks'
    ]

    # REDIS data
    KEY_ = 'songs'
    REDIS_ID = 'profile'

    def __init__(self, id_):
        ENCall.__init__(self, self.TYPE_, self.METHOD, id_, self.BUCKETS)
        self.payload['id'] = id_


    def trim(self, data):
        # song search returns a list. we're using an id so we'll always use the first item
        if len(data) == 0:
            return data
        else:
            data = data[0]

        result = {}

        if 'title' in data:
            result['title'] = data['title']

        if 'artist_name' in data:
            result['artist_name'] = data['artist_name']

        if 'artist_id' in data:
            result['artist_id'] = data['artist_id']
            
        if 'audio_summary' in data:
            result['audio_summary'] = data['audio_summary']

            song_duration = data['audio_summary']['duration'] / 60
            song_duration = str(round(song_duration,2))
            song_duration = song_duration.replace('.', ':')

            result['duration'] = song_duration

        if 'song_hotttnesss_rank' in data:
            result['rank'] = data['song_hotttnesss_rank']

        if 'song_hotttnesss' in data:
            result['hotttnesss'] = int(round(data['song_hotttnesss'] * 100))

        return result

        # if len(data) > 0:
        #     data = data[0]
            
        # if 'song_hotttnesss' in data:
        #     data['song_hotttnesss'] = int(round(data['song_hotttnesss'] * 100))

        # return data
