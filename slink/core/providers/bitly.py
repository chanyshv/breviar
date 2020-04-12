import requests
import cerberus

from ...core.errors import WrongResponse
from ...core.utils import reraise_requests
from ..main import Provider


class BitlyProvider(Provider):
    _SHORTEN_API_URL = 'https://api-ssl.bitly.com/v4/shorten'
    _RESPONSE_SCHEMA = {'link': {'type': 'string'}}

    def __init__(self, access_token: str):
        self._access_token = access_token

    @reraise_requests
    def shorten_url(self, url: str) -> str:
        data = {
            'long_url': url,
        }
        headers = {
            'Authorization': f'Bearer {self._access_token}',
            'Accept': 'application/json',
        }
        # todo: add general timeout
        resp = requests.post(self._SHORTEN_API_URL, headers=headers, json=data, timeout=5)
        json_resp = resp.json()
        is_valid = cerberus.Validator(self._RESPONSE_SCHEMA, allow_unknown=True).validate(json_resp)
        if not is_valid:
            raise WrongResponse
        return json_resp['link']
