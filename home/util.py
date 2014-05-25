# bios = list of artist biographies
# return one with min < len < max
def get_good_bio(bios, min, max):
    #optimize
    if len(bios[0]['text']) > min and len(bios[0]['text']) < max:
        return (bios[0]['text'])
    else:
        #check all bios for something acceptable
        for b in bios:
            if len(b['text']) > min and len(b['text']) < max:
                return (b['text'])

        return 'Artist biography is not available.'

# These two functions can easily be combined.
# Have artist and song objects implement an
# interface which returns the 'title' (name)
# or (title) of the object.  Replace the
# name/title calls with the interface getter.
# I need to research how interfaces in python.

#remove duplicates from list and return len = n
#returns n = len(inc_list) if len < n
def remove_duplicate_artists(inc_list, n):
    trunc_list = []
    temp = []

    for i in inc_list:
        if i.name not in temp:
            temp.append(i.name)
            trunc_list.append(i.name)

        if len(trunc_list) == n:
            break

    return trunc_list

# remove duplicates from list and return len = n
# returns n = len(inc_list) if len < n
def remove_duplicate_songs(inc_list, n):
    trunc_list = []
    temp = []

    for i in inc_list:
        if i.title not in temp:
            temp.append(i.title)
            trunc_list.append(i.title)

        if len(trunc_list) == n:
            break

    return trunc_list

# take a list of five artists, return a list containing the two most popular songs per artist
def get_similar_songs(inc_list):
    similar_songs = []
    temp = []

    for a in inc_list:
        for x in range(0,2):  
            if a.songs[x].title not in temp:
                temp.append(a.songs[x].title)
                similar_songs.append(a.songs[x].title)

    return similar_songs[:10]