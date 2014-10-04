"""Remove unused data from echo nest API responses."""
from __future__ import absolute_import


REJECTED_IMAGES = set([u'myspace', u'thumb',])


def genres(genre_dicts, count=None):
    trimmed = []
    count = count or len(genre_dicts)

    for genre in genre_dicts[:count]:
        genre_text = genre.get('name')

        if genre_text:
            trimmed.append(genre_text)

    return trimmed


def images(image_dicts, count=None):
    trimmed = []
    count = count or len(image_dicts)

    for img in image_dicts:
        url = img.get('url', '')

        if not any(bad_src in url for bad_src in REJECTED_IMAGES):
            if url:
                trimmed.append(url)
            if len(trimmed) >= count:
                break

    return trimmed


def rank(hotttnesss):
    hotttnesss = hotttnesss or 0.0

    if hotttnesss is not float:
        try:
            hotttnesss = float(hotttnesss)
        except TypeError:
            return None
            
    return round(hotttnesss * 100, 2)


def songs(song_dicts, count=None):
    trimmed = []
    count = count or len(song_dicts)
    seen = set('DEFAULT')

    for song in song_dicts:
        title = song.get('title', 'DEFAULT')
        
        # Remove identical songs with different echo nest IDs
        if title not in seen:
            seen.add(title)
            trimmed.append(song)
        if len(trimmed) >= count:
            break

    return trimmed
