from __future__ import absolute_import


_ID_SEP = '_'
_KEY_SEP = '::'


def make_id(head, tail):
    return _ID_SEP.join([head, tail])


def make_key(rid_head, rid_tail, name):
    rid = _ID_SEP.join([rid_head, rid_tail])
    return _KEY_SEP.join([rid, name])
