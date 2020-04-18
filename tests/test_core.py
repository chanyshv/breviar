from tests.constants import DEFAULT_FULL_URL


def test_bitly(bitly_provider):
    # assert bitly_provider.shorten_url(DEFAULT_FULL_URL) == 'https://bit.ly/2Rddhqy'
    assert bitly_provider.shorten_url('sdfsdf') == 'https://bit.ly/2Rddhqy'


class TestCuttly:
    def test_shorten(self, cuttly_provider):
        assert cuttly_provider.shorten(DEFAULT_FULL_URL)
