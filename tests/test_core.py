import os

from slink.core import BitlyProvider
from tests.constants import DEFAULT_FULL_URL


def test_bitly(mock_bitly_response):
    assert BitlyProvider(os.getenv('BITLY_ACCESS_TOKEN')).shorten_url(DEFAULT_FULL_URL) == 'https://bit.ly/2Rddhqy'
