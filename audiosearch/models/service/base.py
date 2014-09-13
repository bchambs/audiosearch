from __future__ import absolute_import

from audiosearch import conf


class EchoNestService(object):
    _lead = 'http://developer.echonest.com/api'
    _version = 'v4'
    _format = 'json'
    max_results = 100   # Largest size result for Echo Nest responses.


    def __init__(self, type_, method, payload, **kwargs):
        self.dependency_ = kwargs.get('dependency')
        self._url = '/'.join([EchoNestService._lead, EchoNestService._version, 
            type_, method])
        self._payload = {
            'api_key': conf.ECHO_API_KEY,
            'format': EchoNestService._format,
        }
        self._payload.update(payload)


    def __repr__(self):
        return "%s %s service" % (self._type, self._method)


    @property
    def echo_key(self):
        return self.echo_key


    @property
    def dependency(self):
        return self.dependency_


    @property
    def payload(self):
        return self._payload


    @property
    def url(self):
        return self._url



