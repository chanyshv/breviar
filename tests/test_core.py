from slink.core import BitlyClient
from tests.constants import DEFAULT_FULL_URL


def test_bitly(mock_bitly_response):
    assert BitlyClient().shorten_url(DEFAULT_FULL_URL) == 'https://bit.ly/2Rddhqy'
