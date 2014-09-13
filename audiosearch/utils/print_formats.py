from __future__ import absolute_import


def fprint_dict(title, d, depth=1):
    offset = (' ' * 4) * depth
    indent = offset + (' ' * 4)

    print '\n{}{}'.format(offset, title)
    for k, v in d.iteritems():
        print '{}{}: {}'.format(indent, k, v) 
    print

