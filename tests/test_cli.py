from click.testing import CliRunner
import pytest

from slink.cli import slink


@pytest.mark.skip('tests data is mocked')
def test_bitly_shorten(mock_bitly_config, mock_bitly_response):
    runner = CliRunner()
    res = runner.invoke(slink, 'shorten -S bitly https://google.com')
    assert res.exit_code == 0
    assert res.output == 'https://bit.ly/2Rddhqy\n'
