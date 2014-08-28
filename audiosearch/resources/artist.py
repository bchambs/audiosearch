from __future__ import absolute_import

from audiosearch.resources.base import BaseResource 
"""
content
    artist.py
    playlist.py
    song.py
    search.py
    top.py

resources
    profile
    similar
    playlist
    top
    songs
"""   

class Artist(BaseResource):
    _content_id = 'artist'


class Profile(Artist):
     _resource_id = 'profile'


     def __init__(self, name):
        self.name = name
        self.type_ = _content_id + _resource_id


