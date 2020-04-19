import responses

from slink.core import CuttlyProvider
from tests import constants
from tests.constants import DEFAULT_FULL_URL, CUTTLY_SHORTENED_URL
from slink.core.errors import ProviderError, WrongResponse

import pytest


def test_bitly(bitly_provider, mock_bitly):
    assert bitly_provider.shorten_url(DEFAULT_FULL_URL) == 'https://bit.ly/2Rddhqy'


class TestCuttly:
    def test_shorten_success(self, cuttly_provider, mock_cuttly_success):
        assert cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_cuttly_fail_status(self, cuttly_provider):
        with responses.RequestsMock() as rsps:
            rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.CUTTLY_FAIL_RESPONSE_DATA).read())
            with pytest.raises(ProviderError):
                cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_cuttly_invalid_response(self, cuttly_provider):
        with pytest.raises(WrongResponse):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.INVALID_DATA).read())
                cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_invalid_json(self, cuttly_provider):
        with pytest.raises(WrongResponse):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.INVALID_JSON_DATA).read())
                cuttly_provider.shorten(DEFAULT_FULL_URL)

    def test_stats(self, cuttly_provider, mock_cuttly_stats_success):
        assert cuttly_provider.stats(CUTTLY_SHORTENED_URL)

    def test_cuttly_stats_fail_status(self, cuttly_provider):
        with pytest.raises(ProviderError):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.CUTTLY_STATS_FAIL_STATUS_DATA).read())
                cuttly_provider.stats(CUTTLY_SHORTENED_URL)

    def test_cuttly_stats_invalid_response(self, cuttly_provider):
        with pytest.raises(WrongResponse):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.INVALID_DATA).read())
                cuttly_provider.stats(CUTTLY_SHORTENED_URL)

    def test_cuttly_stats_invalid_json(self, cuttly_provider):
        with pytest.raises(WrongResponse):
            with responses.RequestsMock() as rsps:
                rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.INVALID_DATA).read())
                cuttly_provider.stats(CUTTLY_SHORTENED_URL)
