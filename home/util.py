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
    temp = []

    for i in inc_list:
        if i.name not in temp:
            temp.append(i.name)
            trunc_list.append(i.name)

        if len(trunc_list) == size:
            break
    return trunc_list

#remove duplicates from list and return len = size
#returns size = len(inc_list) if len < size
def remove_duplicate_songs(inc_list, size):
    print "incoming list"
    for a in inc_list:
        print a
    print

    trunc_list = []
    temp = []

    for i in inc_list:
        if i.title not in temp:
            temp.append(i.title)
            trunc_list.append(i.title)

        if len(trunc_list) == size:
            break

    print "outgoing list"
    for b in trunc_list:
        print b
    print

    return trunc_list

#take a list of five artists, return a list containing the two most popular songs per artist
def get_similar_songs(inc_list):
    similar_songs = []

    for a in inc_list:
        for x in range(0,2):
            if a.songs[x] and a.songs[x] not in similar_songs:
                similar_songs.append(a.songs[x].title)

    return similar_songs[:10]