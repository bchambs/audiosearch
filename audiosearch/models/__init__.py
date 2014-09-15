from __future__ import absolute_import


_ID_SEP = '+'
_KEY_SEP = '::'


def make_id(head, tail):
    return _ID_SEP.join([head, tail])


def make_key(key_id, name):
    return _KEY_SEP.join([key_id, name])
