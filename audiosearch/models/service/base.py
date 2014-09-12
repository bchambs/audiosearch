from __future__ import absolute_import

from audiosearch import conf


class EchoNestService(object):
    LEAD = 'http://developer.echonest.com/api'
    VERSION = 'v4'
    FORMAT = 'json'
    max_results = 100   # Largest size result for Echo Nest responses.


    def __init__(self, type_, method, payload, **kwargs):
        self.dependency_ = kwargs.get('dependency')
        self._url = '/'.join([EchoNestService.LEAD, EchoNestService.VERSION, 
            type_, method])
        self._payload = {
            'api_key': conf.ECHO_API_KEY,
            'format': EchoNestService.FORMAT,
        }
        self._payload.update(payload)


    def __repr__(self):
        return "%s %s service" % (self.TYPE_, self.METHOD)


    @property
    def echo_key(self):
        return self.ECHO_NEST_KEY


    @property
    def dependency(self):
        return self.dependency_


    @property
    def payload(self):
        return self._payload


    @property
    def url(self):
        return self._url



