import os

import requests


class BitlyClient:
    _SHORTEN_API_URL = 'https://api-ssl.bitly.com/v4/shorten'

    def shorten_url(self, url: str) -> str:
        data = {
            'long_url': url,
        }
        headers = {
            'Authorization': f'Bearer {os.getenv("BITLY_ACCESS_TOKEN")}',
            'Accept': 'application/json',
        }
        resp = requests.post(self._SHORTEN_API_URL, headers=headers, json=data, timeout=5)
        return resp.json()['link']
