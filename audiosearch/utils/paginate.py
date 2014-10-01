from __future__ import absolute_import

from audiosearch.conf.display import ROWS_PER_TABLE as INTERVAL


def calculate_offset(page, total_pages, data_length):
    start, end = paginate(page, data_length)
    return start + 1
    

# redis list are closed-interval
def paginate(page, data_length):
    if page < 2:
        start = 0
        end = INTERVAL - 1
    else:
        check = (page - 1) * INTERVAL
        if check >= data_length:
            start = 0
            end = INTERVAL - 1
        else:
            start = check
            end = start + INTERVAL - 1


    return start, end


def dbg(page, start, end):
    print "    GETTING LIST    "
    print "         page: {}".format(page)
    print "         start: {}".format(start)
    print "         end: {}".format(end)
