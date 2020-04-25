import requests
import cerberus

from ...core.errors import WrongResponse, Forbidden, breviarError
from ...core.utils import reraise_requests
from ..main import Provider


class BitlyError(breviarError):
    def __init__(self, error_message: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = f'Bitly error. Error message :"{error_message}"'


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
        if resp.status_code == 403:
            raise Forbidden
        if resp.status_code in (400, 402, 403, 404, 417, 422):
            raise BitlyError(resp.json()['description'])
        json_resp = resp.json()
        is_valid = cerberus.Validator(self._RESPONSE_SCHEMA, allow_unknown=True, require_all=True).validate(json_resp)
        if not is_valid:
            raise WrongResponse
        return json_resp['link']
