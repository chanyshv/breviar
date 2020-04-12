import os

import pytest
import responses
from mock_open import MockOpen

from slink.core import BitlyProvider
from slink.cli.constants import BITLY_CONFIG_PATH
from tests import constants


def pytest_addoption(parser):
    parser.addoption('--mock', action='store', default=False)


@pytest.fixture(scope='package')
def mock_argument(pytestconfig):
    return int(pytestconfig.getoption('--mock'))


@pytest.fixture()
def mock_bitly():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BitlyProvider._SHORTEN_API_URL, open(constants.BITLY_DATA).read())
        yield rsps


@pytest.fixture()
def bitly_provider(mock_argument):
    return BitlyProvider(os.getenv('BITLY_ACCESS_TOKEN'))


@pytest.fixture()
def mock_bitly_config(monkeypatch):
    mock_open = MockOpen()
    mock_open[BITLY_CONFIG_PATH].read_data = open(constants.BITLY_CONFIG_PATH).read()
    monkeypatch.setattr('builtins.open', MockOpen)
