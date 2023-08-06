from pathlib import Path

import pytest

from webdomains.core import (
    BaseDomain,
    ConfigurationError,
    get_nginx_directive_value,
)


class DummyDomain(BaseDomain):
    conf_dir = Path('/etc/dummy/available')
    enabled_conf_dir = Path('/etc/dummy/enabled')

    @property
    def conf_path(self):
        return self.conf_dir / self.name

    @property
    def enabled_conf_path(self):
        return self.enabled_conf_dir / self.name


class TestNGINXHelpers:
    def test_get_nginx_directive_value(self):
        conf = """
server {
  server_name domain.tld www.domain.tld;
}
"""

        assert (
            get_nginx_directive_value('server_name', conf)
            == 'domain.tld www.domain.tld'
        )

    def test_get_nginx_directive_value_error(self):
        with pytest.raises(ConfigurationError) as excinfo:
            get_nginx_directive_value('test', "some configuration")
        assert str(excinfo.value) == "`test` directive is not defined."


class TestBaseDomainConf:
    @pytest.fixture(autouse=True)
    def setup_domain(self):
        self.domain = DummyDomain('test.example.org')

    def test_get_property_from_conf(self):
        conf = """
## protocol=http
## empty=
## spaces = value
 ## indent=value
"""  # noqa: W291

        assert self.domain.get_property_from_conf(conf, 'protocol') == 'http'
        assert self.domain.get_property_from_conf(conf, 'empty') == ''

        with pytest.raises(ConfigurationError):
            self.domain.get_property_from_conf(conf, 'spaces')
        with pytest.raises(ConfigurationError):
            self.domain.get_property_from_conf(conf, 'indent')

    def test_get_property_from_conf_pattern(self):
        conf = """
## protocol=http
## invalid=http1
## empty=
"""

        assert (
            self.domain.get_property_from_conf(conf, 'protocol', r'[a-z]+')
            == 'http'
        )

        with pytest.raises(ConfigurationError):
            self.domain.get_property_from_conf(conf, 'invalid', r'[a-z]+')
        with pytest.raises(ConfigurationError):
            self.domain.get_property_from_conf(conf, 'empty', r'.+')

    def test_get_property_from_conf_not_defined(self):
        with pytest.raises(ConfigurationError) as excinfo:
            self.domain.get_property_from_conf("some configuration", 'test')
        assert excinfo.value.message == "`test` variable is not defined."
