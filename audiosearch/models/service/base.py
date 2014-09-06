from __future__ import absolute_import

from audiosearch import conf




class Error(Exception):
    pass

class ServiceError(Error):
    pass

class EmptyResponseError(Error):
    pass


class EchoNestService(object):
    _LEAD = "http://developer.echonest.com/api"
    _VERSION = "v4"
    _FORMAT = 'json'
    _RESULT_MAX_LEN = 100   # Largest size result for Echo Nest responses.


    def __init__(self, type_, method, payload, **kwargs):
        self._dependencies = kwargs.get('dependencies')
        self._url = '/'.join([self._LEAD, self._VERSION, type_, method])
        self._payload = {
            'api_key': conf.API_KEY,
            'format': EchoNestService._FORMAT,
        }
        self._payload.update(payload)

    def __str__(self):
        return "EchoNestService"

    @property
    def dependencies(self):
        return self._dependencies

    @property
    def payload(self):
        return self._payload

    @property
    def url(self):
        return self._url
