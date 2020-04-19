import requests as rq
import cerberus

from ..main import Provider
from ..errors import WrongResponse, ProviderError
from ..utils import reraise_requests


class CuttlyProvider(Provider):
    _SHORTEN_STATUS_MAP = {
        1: 'the link has already been shortened',
        2: 'the entered link is not a link',
        3: 'the preferred link name is already taken',
        4: 'Invalid API key',
        5: 'the link has not passed the validation.Includes invalid characters',
        6: 'The link provided is from a blocked domain',
        7: 'OK - the link has been shortened',
    }
    _STATS_STATUS_MAP = {
        0: 'This shortened link does not exist',
        1: 'This link exists and the data has been downloaded',
        2: 'Invalid API key',
    }
    _SHORTEN_RESPONSE_SCHEMA = {
        'url': {'type': 'dict', 'schema': {'status': {'type': 'integer'}}}
    }
    _STATS_RESPONSE_SCHEMA = {
        'stats': {'type': 'dict', 'schema': {'status': {'type': 'integer'},
                                             'clicks': {'type': 'string'},
                                             'date': {'type': 'string'},
                                             'title': {'type': 'string'},
                                             'fullLink': {'type': 'string'},
                                             }}}
    _API_URL = 'https://cutt.ly/api/api.php'

    def __init__(self, api_key: str):
        self._api_key = api_key

    def _validate_response(self, r: rq.Response, validation_schema: dict):
        if not r.text:
            raise WrongResponse
        try:
            json_r = r.json()
        except ValueError as e:
            raise WrongResponse from e
        validator = cerberus.Validator(validation_schema, allow_unknown=True, require_all=True)
        is_valid = validator.validate(json_r)
        if not is_valid:
            raise WrongResponse

    def _validate_status(self, status: int, success_status: int, status_map: dict):
        if status not in status_map:
            raise WrongResponse
        if status != success_status:
            raise ProviderError('cuttly', status_map[status])

    @reraise_requests
    def shorten(self, url: str) -> str:
        data = {
            'short': url,
            'key': self._api_key,
        }
        r = rq.get(self._API_URL, params=data)
        self._validate_response(r, self._SHORTEN_RESPONSE_SCHEMA)
        json_r = r.json()
        self._validate_status(json_r['url']['status'], 7, self._SHORTEN_STATUS_MAP)
        return json_r['url']['shortLink']

    @reraise_requests
    def stats(self, url: str):
        data = {
            'key': self._api_key,
            'stats': url,
        }
        r = rq.get(self._API_URL, params=data)
        json_r = r.json()
        self._validate_response(r, self._STATS_RESPONSE_SCHEMA)
        self._validate_status(json_r['stats']['status'], 1, self._STATS_STATUS_MAP)
        stats = json_r['stats']
        return {
            'title': stats['title'],
            'clicks': stats['clicks'],
            'short_link': stats['shortLink'],
            'full_link': stats['fullLink'],
            'date': stats['date'],
            'stats_link': stats['shortLink'] + '-stats',
        }
