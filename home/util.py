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

# remove duplicates from list and return len = n
# returns n = len(inc_list) if len < n
def remove_duplicates (inc_list, n):
    trunc_list = []
    temp = {}

    for i in inc_list:
        if str(i).lower() not in temp:
            temp[str(i).lower()] = 1
            trunc_list.append(i)

        if len(trunc_list) == n:
            break

    return trunc_list

# remove duplicates from list and return len = n
# returns n = len(inc_list) if len < n
# def remove_duplicate_artists(inc_list, n):
#     trunc_list = []
#     temp = {}

#     for i in inc_list:
#         if i.name not in temp:
#             temp[i.name] = 1
#             trunc_list.append(i.name)

#         if len(trunc_list) == n:
#             break

#     return trunc_list

# take a list of five artists, return a list containing the two most popular songs per artist
def get_similar_songs(inc_list):
    similar_songs = []
    temp = {}

    for a in inc_list:
        #boundary check range of song list
        if len(a.songs) < 2:
            song_range = len(a.songs)
        else:
            song_range = 2

        for x in range(0,song_range):  
            if a.songs[x].title.lower() not in temp:
                temp[a.songs[x].title.lower()] = 1      # make this more legible
                similar_songs.append(a.songs[x].title)

    return similar_songs[:10]