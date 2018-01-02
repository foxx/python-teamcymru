import pytest

from teamcymru import IPResult, IPToASN


class TestIPToASN():
    """
    Test `IPToASN` functionality
    """

    def test_empty_ips_list(self):
        ips = []
        with pytest.raises(ValueError):
            i2a = IPToASN(ips)

    def test_malformed_ip_addresse(self):
        ips = [""]
        with pytest.raises(ValueError):
            IPToASN(ips)

        ips = ["sadfadsf"]
        with pytest.raises(ValueError):
            IPToASN(ips)

    def test_correct_ipv4_addresses(self):
        ips = ["68.22.187.5", "207.229.165.18", "105.111.29.252"]

        i2a = IPToASN(ips)
        result = i2a.lookup()
        assert len(result) == 3
        for item in result:
            assert isinstance(item, IPResult)
            assert not item.has_error()

    def test_correct_ipv6_addresses(self):
        ips = ['2001:db8:85a3::8a2e:370:7334', 'fe80:3::1ff:fe23:4567:890a']

        i2a = IPToASN(ips)
        result = i2a.lookup()
        assert len(result) == 2
        for item in result:
            assert isinstance(item, IPResult)
            assert not item.has_error()

    def test_mix_of_ipv4_ip6_addresses(self):
        ips = ['2001:db8:85a3::8a2e:370:7334', "68.22.187.5"]
        i2a = IPToASN(ips)
        result = i2a.lookup()
        assert len(result) == 2
        for item in result:
            assert isinstance(item, IPResult)
            assert not item.has_error()

    def test_correct_but_bad_ip_addresses(self):
        """
        XXX: this is just to make sure, whois.cymru.com doesn't really care :)
        """
        ips = ['0.0.0.0', '127.0.0.1', '192.168.1.1']
        i2a = IPToASN(ips)
        result = i2a.lookup()
        assert len(result) == 3
        for item in result:
            assert isinstance(item, IPResult)

    def test_cached_results(self):
        ips = ["68.22.187.5", "207.229.165.18", "105.111.29.252"]
        i2a = IPToASN(ips)
        result = i2a.lookup()
        assert len(result) == 3
        assert i2a.hits == 1

        result2 = i2a.lookup()
        assert len(result2) == 3
        assert i2a.hits == 1

        # test refresh
        result3 = i2a.lookup(refresh=True)
        assert len(result2) == 3
        assert i2a.hits == 2
