from __future__ import absolute_import

from audiosearch import conf


class EchoNestService(object):
    _LEAD = 'http://developer.echonest.com/api'
    _VERSION = 'v4'
    _FORMAT = 'json'
    _RESULT_MAX_LEN = 100   # Largest size result for Echo Nest responses.
    url = _LEAD


    def __init__(self, type_, method, payload, **kwargs):
        self.dependency_ = kwargs.get('dependency')
        self._url = '/'.join([EchoNestService._LEAD, EchoNestService._VERSION, 
            type_, method])
        self._payload = {
            'api_key': conf.ECHO_API_KEY,
            'format': EchoNestService._FORMAT,
        }
        self._payload.update(payload)


    def __repr__(self):
        return "%s %s service" % (self.TYPE_, self.METHOD)


    @property
    def dependency(self):
        return self.dependency_


    @property
    def payload(self):
        return self._payload


    @property
    def url(self):
        return self._url



