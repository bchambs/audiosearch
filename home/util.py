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