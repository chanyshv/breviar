import pytest
import responses
from mock_open import MockOpen

from slink.core import BitlyProvider
from slink.cli.constants import BITLY_CONFIG_PATH
from tests import constants


@pytest.fixture()
def mock_bitly_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BitlyProvider._SHORTEN_API_URL, open(constants.BITLY_DATA).read())
        yield rsps


@pytest.fixture()
def mock_bitly_config(monkeypatch):
    mock_open = MockOpen()
    mock_open[BITLY_CONFIG_PATH].read_data = open(constants.BITLY_CONFIG_PATH).read()
    monkeypatch.setattr('builtins.open', MockOpen)
