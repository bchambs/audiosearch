from __future__ import absolute_import
from itertools import chain

from audiosearch.conf import echonest_api


class BaseService(object):

    def __init__(self, 
        group, 
        method,
        response_key,
        bucket=None, 
        dependencies=None, 
        params=None, 
        trim=False):

        # Default lists and dicts
        dependencies = [] if dependencies is None else dependencies
        params = {} if params is None else params

        # Build request payload
        params = chain(echonest_api.BASE_PARAMS.iteritems(), params.iteritems())
        if bucket:
            params['bucket'] = bucket

        url = '/'.join([echonest_api.BASE_URL, group, method])

        self.dependencies = dependencies
        # self.group = group
        # self.method = method
        self.params = params
        self.response_key = response_key
        self.trim = trim
        self.url = url


    def __repr__(self):
        return "%s %s service" % (self.group, self.method)


class Artist(BaseService):
    pass


class Top(BaseService):
    keys = dict(artists='artists')
    valid_groups = set(['artists'])


    def __init__(self, group):
        if group not in Top.valid_groups:
            raise ValueError('Unexpected group')

        content = ['hotttnesss_rank']
        key = Top.keys[group]
        method = 'top_hottt'

        super(Top, self).__init__(
            group,
            method,
            key,
            bucket=content,
        )


def create_service_map():
    service_map = {

    }

    def init_service(group, method, params):
        return service_map[group][method](**params)
    return init_service

Factory = create_service_map()


# class SongID(EchoNestService):
#     """Used to acquire a song's Echo Nest id."""
#     group = 'song'
#     method = 'search'
#     response_key = 'songs'


#     def __init__(self, artist, song):
#         params = dict(results=1, songgroup=None)
#         super(SongID, self).__init__(SongID.group, SongID.method, **params)


#     def __repr__(self):
#         tail = " (dependency)"
#         return super(SongID, self).__repr__() + tail



# ###############################################################################
# ###############################################################################
# ###############################################################################
# class ArtistProfile(EchoNestService):
#     group = 'artist'
#     method = 'profile'
#     bucket = [
#         'artist_location',
#         'biographies',
#         'images',
#         'hotttnesss',
#         'genre',
#         'years_active',
#     ]
#     requires_processing = True
#     response_key = 'artist'


#     def __init__(self, artist):
#         params = dict(name=artist, bucket=ArtistProfile.bucket)
#         super(ArtistProfile, self).__init__(ArtistProfile.group, 
#                                             ArtistProfile.method, **params)
            

#     # redo
#     def process(self, raw_data):
#         data = {}

#         # Artist location.
#         try:
#             location_wrap = raw_data.pop('artist_location')
#             data['location'] = location_wrap.pop('location')
#         except KeyError:
#             pass

#         # Genre tags.
#         try:
#             genres = raw_data.pop('genres')
#         except KeyError:
#             pass
#         else:
#             data['genres'] = []

#             for genre in genres[:GENRE_COUNT]:
#                 data['genres'].append(genre['name'])

#         # Years active.
#         try:
#             years_active_wrap = raw_data.pop('years_active')
#             years_active = years_active_wrap.pop()
#         except IndexError, KeyError:
#             pass
#         else:
#             start = years_active.get('start', "Unknown")
#             end = years_active.get('end', "Present")

#             data['years_active'] = "(%s - %s)" %(start, end)

#         # Image urls.
#         try:
#             image_wrap = raw_data.pop('images')
#             image = image_wrap.pop()
#             data['image'] = image.pop('url')
#         except (IndexError, KeyError):
#             pass

#         return data


# class ArtistSongs(EchoNestService):
#     group = 'playlist'
#     method = 'static'
#     bucket = [
#         'audio_summary',
#     ]
#     response_key = 'songs'


#     def __init__(self, artist):
#         params = {
#             'artist': artist,
#             'results': EchoNestService.max_results,
#             'sort': "song_hotttnesss-desc",
#         }
#         super(ArtistSongs, self).__init__(ArtistSongs.group, ArtistSongs.method,
#                                             **params)


# class SearchArtists(EchoNestService):
#     group = 'artist'
#     method = 'suggest'
#     response_key = 'artists'


#     def __init__(self, artist):
#         params = dict(name=artist)
#         super(SearchArtists, self).__init__(SearchArtists.group, 
#                                             SearchArtists.method, **params)


# class SimilarArtists(EchoNestService):
#     group = 'artist'
#     method = 'similar'
#     bucket = [
#         'images',
#         'terms',
#         'songs',
#     ]
#     response_key = 'artists'


#     def __init__(self, artist):
#         params = dict(name=artist, bucket=SimilarArtists.bucket)
#         super(ArtistProfile, self).__init__(SimilarArtists.group, 
#                                             SimilarArtists.method, **params)





# ###############################################################################
# ###############################################################################
# ###############################################################################
# class SearchSongs(EchoNestService):
#     group = 'song'
#     method = 'search'
#     bucket = [
#         'song_hotttnesss', 
#         'song_hotttnesss_rank', 
#     ]
#     response_key = 'songs'


#     def __init__(self, artist, song):
#         params = {
#             'artist': artist,
#             'bucket': SearchSongs.bucket,
#             'songgroup': 'studio',
#             'sort': 'song_hotttnesss-desc',
#             'title': song,
#         }
#         super(SearchSongs, self).__init__(SearchSongs.group, 
#                                             SearchSongs.method, **params)


# class SongProfile(EchoNestService):
#     group = 'song'
#     method = 'profile'
#     bucket = [
#         'audio_summary',
#         'song_hotttnesss', 
#         'song_hotttnesss_rank', 
#         'songgroup',
#     ]
#     response_key = 'songs'


#     def __init__(self, artist, song):
#         params = dict(bucket=SongProfile.bucket)
#         super(SongProfile, self).__init__(SongProfile.group, 
#                                             SongProfile.method, **params)
#         id_service = SongID(song, artist)
#         self.dependencies.append(id_service)




# ###############################################################################
# ###############################################################################
# ###############################################################################
# class BasePlaylist(EchoNestService):
#     group = 'playlist'
#     method = 'static'
#     bucket = [
#         'song_hotttnesss',
#     ]
#     response_key = 'songs'
    

#     def __init__(self, params):
#         super(BasePlaylist, self).__init__(BasePlaylist.group, 
#                                             BasePlaylist.method, **params)


# class SongPlaylist(BasePlaylist):
#     bucket = [
#         'audio_summary',
#     ]


#     def __init__(self, artist, song):
#         bucket = BasePlaylist.bucket + SongPlaylist.bucket
#         params = dict(type='song-radio', bucket=bucket)
#         super(SongPlaylist, self).__init__(params)
#         id_service = SongID(song, artist)
#         self.dependencies.append(id_service)


#     # def combine_dependency(self, intermediate):
#     #     try:
#     #         first_result = intermediate.pop()
#     #         self.params['song_id'] = first_result.pop('id')
#     #     except (IndexError, KeyError):
#     #         raise EmptyResponseError()


# class ArtistPlaylist(BasePlaylist):

#     def __init__(self, artist):
#         params = dict(artist=artist, variety=1, type='artist-radio')
#         super(ArtistPlaylist, self).__init__(params)



# ###############################################################################
# ###############################################################################
# ###############################################################################
# '''move this somewhere'''
# def create_service_map():
#     service_map = {
#         'artist': {
#             'playlist': ArtistPlaylist,
#             'profile': ArtistProfile,
#             'similar': SimilarArtists,
#             'songs': ArtistSongs,
#         },
#         'song': {
#             'profile': SongProfile,
#             'playlist': SongPlaylist,
#         },
#         'search': {
#             'artists': SearchArtists,
#             'songs': SearchSongs,
#         },
#         'top': {
#             'artists': TopArtists,
#         },
#     }

#     def init_service(echonest_group, contentgroup, params):
#         return service_map[echonest_group][contentgroup](**params)
#     return init_service

# factory = create_service_map()
