from tests.constants import DEFAULT_FULL_URL


def test_bitly(bitly_provider, mock_bitly):
    assert bitly_provider.shorten_url(DEFAULT_FULL_URL) == 'https://bit.ly/2Rddhqy'
