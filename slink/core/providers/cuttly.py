import requests as rq
import cerberus

from ..main import Provider
from ..errors import WrongResponse, ProviderError
from ..utils import reraise_requests


class CuttlyProvider(Provider):
    _STATUS_MAP = {
        1: 'the link has already been shortened',
        2: 'the entered link is not a link',
        3: 'the preferred link name is already taken',
        4: 'Invalid API key',
        5: 'the link has not passed the validation.Includes invalid characters',
        6: 'The link provided is from a blocked domain',
        7: 'OK - the link has been shortened',
    }
    _RESPONSE_SCHEMA = {
        'url': {'type': 'dict', 'schema': {'status': {'type': 'integer'}}}
    }
    _API_URL = 'https://cutt.ly/api/api.php'

    def __init__(self, api_key: str):
        self._api_key = api_key

    @reraise_requests
    def shorten(self, url: str) -> str:
        data = {
            'short': url,
            'key': self._api_key,
        }
        r = rq.get(self._API_URL, params=data)
        if not r.text:
            raise WrongResponse
        validator = cerberus.Validator(self._RESPONSE_SCHEMA, allow_unknown=True, require_all=True)
        try:
            json_r = r.json()
        except ValueError as e:
            raise WrongResponse from e
        is_valid = validator.validate(json_r)
        if not is_valid:
            raise WrongResponse
        status = json_r['url']['status']
        if status not in self._STATUS_MAP:
            raise WrongResponse
        if status != 7:
            raise ProviderError('cuttly', self._STATUS_MAP[status])
        return json_r['url']['shortLink']
