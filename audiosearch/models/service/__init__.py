
from __future__ import absolute_import

from audiosearch.models.service.artist import (ArtistProfile, ArtistSongs, 
                                                SearchArtists, SimilarArtists, 
                                                TopArtists)
from audiosearch.models.service.playlist import SongPlaylist, ArtistPlaylist
from audiosearch.models.service.song import SearchSongs, SongProfile
from audiosearch.models.service.consumer import (consume, ServiceFailureError, 
                                                TimeoutError)

def create_service_map():
    import os
    print '\nbuilding service map @ {}'.format(os.getpid())

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


    def get_service(category, content, params):
        return service_map[category][content](**params)
    return get_service

ServiceFactory = create_service_map()
