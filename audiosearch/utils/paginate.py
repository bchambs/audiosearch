from __future__ import absolute_import

from audiosearch.conf.display import ROWS_PER_TABLE as INTERVAL


# redis list are closed-interval
def paginate(page):
    # page = page or 0

    if page < 2:
        start = 0
        end = INTERVAL - 1
    else:
        start = (page - 1) * INTERVAL
        end = start + INTERVAL - 1

    return start, end


def dbg(page, start, end):
    print "    GETTING LIST    "
    print "         page: {}".format(page)
    print "         start: {}".format(start)
    print "         end: {}".format(end)
