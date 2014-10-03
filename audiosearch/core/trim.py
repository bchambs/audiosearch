from __future__ import absolute_import


REJECTED_IMAGES = set('myspace')


def genres(genre_dicts, count=None):
    genres = []
    count = count or len(genre_dicts)

    for genre in genre_dicts[:count]:
        genre_text = genre.get('name')

        if genre_text:
            genres.append(genre_text)

    return genres

def images(image_dicts, count=None):
    images = []
    count = count or len(image_dicts)

    for img in image_dicts:
        attribution = img.get('attribution', 'n/a')

        if attribution not in REJECTED_IMAGES:
            image_url = img.get('url')

            if image_url:
                images.append(image_url)
            if len(images) >= count:
                break

    return images

def rank(hotttnesss):
    hotttnesss = hotttnesss or 0.0

    if hotttnesss is not float:
        try:
            hotttnesss = float(hotttnesss)
        except TypeError:
            return None
            
    return round(hotttnesss * 100, 2)
