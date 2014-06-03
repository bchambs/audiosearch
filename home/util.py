import random

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




# artists = top 10 similar artists
# similar = list containing 10 randomly chosen songs
#
# create a list containing three songs from each similar artist
# note: this assumes best case of each artist having >= 3 songs
def get_similar_songs(artists):
    similar = []
    temp = {}
    count = 0

    for a in artists:

        # boundary check
        if len(a.songs) < 3:
            song_range = len(a.songs)
        else:
            song_range = 3

        # build dict
        for x in range(0, song_range):  
            temp[count] = a.songs[x]
            count += 1

    # randomly build return list
    for x in range(0, 10):
        key = random.choice (temp.keys())
        s = temp[key]

        similar.append(s)
        del temp[key]

    return similar