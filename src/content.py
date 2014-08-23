from __future__ import absolute_import

import src.services as services





class ContentKeys(object):
    ARTIST_PLAYLIST = "artist_playlist"
    ARTIST_PROFILE = "artist_profile"
    ARTIST_SONGS = "artist_songs"

    FAILED = "::FAILED::"
    PENDING = "::PENDING::"

    SEARCH_ARTISTS = "search_artists"
    SEARCH_SONGS = "search_songs"

    SIMILAR_ARTISTS = "similar_artists"

    SONG_PLAYLIST = "song_playlist"
    SONG_PROFILE = "song_profile"

    TOP_ARTISTS = "top_artists"

CONTENT_KEYS = ContentKeys()


class Prefixes(object):
    ARTIST = "artist"
    SEARCH = "search"
    SONG = "song"
    TOP = "top"
    TRENDING = "trending"

PREFIXES = Prefixes()


