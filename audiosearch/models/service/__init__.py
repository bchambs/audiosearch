'''move this to a module'''

from __future__ import absolute_import

from audiosearch.models.service.artist import (
    ArtistProfile, 
    ArtistSongs, 
    SearchArtists, 
    SimilarArtists, 
    TopArtists)
from audiosearch.models.service.playlist import SongPlaylist, ArtistPlaylist
from audiosearch.models.service.song import SearchSongs, SongProfile


'''move this somewhere'''
def create_service_map():
    import os
    print '\nbuilding service map @ {}\n'.format(os.getpid())

    service_map = {
        'artist': {
            'playlist': ArtistPlaylist,
            'profile': ArtistProfile,
            'similar': SimilarArtists,
            'songs': ArtistSongs,
        },
        'song': {
            'profile': SongProfile,
            'playlist': SongPlaylist,
        },
        'search': {
            'artists': SearchArtists,
            'songs': SearchSongs,
        },
        'top': {
            'artists': TopArtists,
        },
    }

    def init_service(call_type, content_type, params):
        return service_map[call_type][content_type](**params)
    return init_service

ServiceFactory = create_service_map()
