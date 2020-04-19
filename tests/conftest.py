import os

import pytest
import responses
from mock_open import MockOpen

from slink.core import BitlyProvider, CuttlyProvider
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
def mock_cuttly_success():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.CUTTLY_SUCCESS_DATA).read())
        yield rsps


@pytest.fixture()
def mock_cuttly_fail_status():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.CUTTLY_FAIL_RESPONSE_DATA).read())
        yield rsps


@pytest.fixture()
def mock_cuttly_invalid_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.INVALID_DATA).read())
        yield rsps


@pytest.fixture()
def mock_cuttly_invalid_json_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, CuttlyProvider._API_URL, open(constants.INVALID_JSON_DATA).read())
        yield rsps


@pytest.fixture()
def bitly_provider(mock_argument):
    return BitlyProvider(os.getenv('BITLY_ACCESS_TOKEN'))


@pytest.fixture()
def cuttly_provider():
    return CuttlyProvider(os.getenv('CUTTLY_ACCESS_TOKEN'))


@pytest.fixture()
def mock_bitly_config(monkeypatch):
    mock_open = MockOpen()
    mock_open[BITLY_CONFIG_PATH].read_data = open(constants.BITLY_CONFIG_PATH).read()
    monkeypatch.setattr('builtins.open', MockOpen)
