import pytest
import responses
from unittest import mock
import builtins

from slink.core import BitlyClient
from tests.constants import BITLY_DATA


@pytest.fixture()
def mock_bitly_response():
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, BitlyClient._SHORTEN_API_URL, open(BITLY_DATA).read())
        yield rsps


@pytest.fixture()
def mock_open(monkeypatch):
    monkeypatch.setattr(builtins, 'open', mock.MagicMock())
