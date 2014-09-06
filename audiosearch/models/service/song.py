from __future__ import absolute_import

from audiosearch.services import dependency
from audiosearch.services.base import EchoNestService, EmptyResponseError


class SearchSongs(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'search'
    BUCKETS = [
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist, song):
        payload = {
            'artist': artist,
            'bucket': SearchSongs.BUCKETS,
            'song_type': "studio",
            'sort': "song_hotttnesss-desc",
            'title': song,
        }
        super(SearchSongs, self).__init__(self.TYPE_, self.METHOD, 
            payload)

    def __str__(self):
        return "search songs"


class SongProfile(EchoNestService):
    TYPE_ = 'song'
    METHOD = 'profile'
    BUCKETS = [
        'audio_summary',
        'song_hotttnesss', 
        'song_hotttnesss_rank', 
        'song_type',
    ]
    ECHO_NEST_KEY = 'songs'


    def __init__(self, artist, song):
        dependencies = list(dependency.SongID(song, artist))
        payload = dict(bucket=SongProfile.BUCKETS)

        super(SongProfile, self).__init__(self.TYPE_, self.METHOD, 
            payload, dependencies=dependencies)

    def __str__(self):
        return "song profile"

    def combine_dependency(self, intermediate):
        try:
            first_result = intermediate.pop()
            self.payload['song_id'] = first_result.pop('id')
        except (IndexError, KeyError):
            raise EmptyResponseError()

    def process(self, raw_data):
        try:
            first_result = raw_data.pop()
        except IndexError:
            raise EmptyResponseError()
        else:
            data = {}

            # Echo Nest audio analysis.
            try:
                audio = first_result.pop('audio_summary')
            except KeyError:
                pass
            else:
                data['tempo'] = "%s bpm" %(audio.get('tempo'))
                data['danceability'] = to_percent(audio.get('danceability'))
                data['liveness'] = to_percent(audio.get('liveness'))

                # Song duration.
                try:
                    duration = audio.pop('duration')
                    data['duration'] = convert_seconds(duration)
                except KeyError:
                    pass

            # General data.
            data['song_hotttnesss'] = first_result.get('song_hotttnesss')
            data['song_hotttnesss_rank'] = first_result.get('song_hotttnesss_rank')

            return data
            

# TODO: remove index error, move try to caller for None str
def to_percent(float):
    p = round(float * 100)
    percent = str(p).split('.')

    try:
        s =  percent.pop() + " %"
    except IndexError:
        s =  ''

    return s


# Used to display (M:S) duration on song profile.
def convert_seconds(duration):
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    print "t is %s" %(type(duration))
    # time = str(duration)
    # try:
    #     minutes = time.split('.').pop() # this is wrong

    # if len(minutes) > 1:
    #     m = int(minutes) / 60
    #     s = round(duration - (m * 60))
    #     seconds = str(s).split('.')[0]

    #     if len(seconds) < 2:
    #         seconds = seconds + "0"

    #     return "(%s:%s)" %(m, seconds)
    # else:
    #     return "(:%s)" %(minutes[0])

    return ''
