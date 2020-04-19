from tests.constants import DEFAULT_FULL_URL, CUTTLY_SHORTENED_URL
from slink.core.errors import ProviderError, WrongResponse

import pytest


def test_bitly(bitly_provider, mock_bitly):
    assert bitly_provider.shorten_url(DEFAULT_FULL_URL) == 'https://bit.ly/2Rddhqy'


class TestCuttly:
    def test_shorten_success(self, cuttly_provider):
        assert cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_cuttly_fail_status(self, cuttly_provider, mock_cuttly_fail_status):
        with pytest.raises(ProviderError):
            cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_cuttly_invalid_response(self, cuttly_provider, mock_cuttly_invalid_response):
        with pytest.raises(WrongResponse):
            cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_invalid_json(self, cuttly_provider, mock_cuttly_invalid_json_response):
        with pytest.raises(WrongResponse):
            cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_stats(self, cuttly_provider):
        assert cuttly_provider.stats(CUTTLY_SHORTENED_URL)
        ...
