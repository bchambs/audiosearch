#bios = list of artist biographies
#return one with 25 < len < x
def get_good_bio(bios):
    if len(bios[0]['text']) > 200:
        return (bios[0]['text'][:197] + '...')
    else:
        for b in bios:
            if len(b['text']) > 200:
                return (b['text'][:197] + '...')
        return 'Bio not available'

#remove duplicates from list and return len = size
#returns size = len(inc_list) if len < size
def remove_duplicate_artists(inc_list, size):
    trunc_list = []

    for i in inc_list:
        if i.name not in trunc_list:
            trunc_list.append(i.name)

        if len(trunc_list) == size:
            break
    return trunc_list

#remove duplicates from list and return len = size
#returns size = len(inc_list) if len < size
def remove_duplicate_songs(inc_list, size):
    trunc_list = []

    for i in inc_list:
        if i.title not in trunc_list:
            trunc_list.append(i.title)

        if len(trunc_list) == size:
            break
    return trunc_list

#given a list of size n, crop size so they look
#god as 100x100 squares, return list for width
#return width for height
def get_cropped_dimensions (inc_list, n):
    width = []
    height = []

    return width, height