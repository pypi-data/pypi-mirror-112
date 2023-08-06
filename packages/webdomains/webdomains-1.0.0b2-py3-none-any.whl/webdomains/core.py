import os
import re
import subprocess
from enum import Enum
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from .utils import cached_property


class ConfigurationError(Exception):
    """An error in the configuration, optionally located at `conf_path`."""

    def __init__(self, message: str, conf_path: Path = None):
        self.message = message
        self.conf_path = conf_path


# NGINX HELPERS
# -----------------------------------------------------------------------------


def get_nginx_directive_value(name: str, conf: str) -> str:
    """Retrieve a directive value from the given NGINX configuration."""
    match = re.search(r'^[ \t]*%s[ \t]+([^;]+);' % name, conf, re.MULTILINE)
    if match is None:
        raise ConfigurationError("`%s` directive is not defined." % name)
    return match.group(1)


def reload_nginx():
    """Reload NGINX server if the configuration is valid."""
    try:
        subprocess.run(
            ['nginx', '-t', '-q'], stderr=subprocess.PIPE, check=True
        )
    except subprocess.CalledProcessError as e:
        raise subprocess.SubprocessError(
            "The NGINX configuration is invalid:\n{}".format(
                e.stderr.decode().strip()
            )
        )
    else:
        proc = subprocess.run(['systemctl', '-q', 'reload', 'nginx.service'])
        if proc.returncode:
            raise subprocess.SubprocessError(
                "The unit 'nginx.service' fails to reload."
            )


# BASE CLASS AND MIXINS
# -----------------------------------------------------------------------------


class BaseDomain:
    """
    Base class for all domain types.

    A domain is defined by a server name. It can be enabled or disabled, and
    its main configuration can be generated or retrieved.

    Subclasses must define at least the `conf_path` and `enabled_conf_path`
    properties.
    """

    #: Ordered list of directories in which templates are looked for.
    templates_dir = [
        '/etc/webdomains/templates',
        os.path.join(os.path.dirname(__file__), 'templates'),
    ]

    #: The template name to use for the configuration.
    template_name = 'server.conf'

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name

    # DYNAMIC PROPERTIES

    @property
    def conf_path(self) -> Path:
        """The path to the main configuration of the domain."""
        raise NotImplementedError(
            "Subclasses of Domain must provide 'conf_path' property."
        )

    @property
    def enabled_conf_path(self) -> Path:
        """The path to the enabled main configuration of the domain."""
        raise NotImplementedError(
            "Subclasses of Domain must provide 'enabled_conf_path' property."
        )

    @property
    def exists(self) -> bool:
        """Whether the domain is defined."""
        return self.conf_path.exists()

    @property
    def is_enabled(self) -> bool:
        """Whether the domain is enabled."""
        return self.enabled_conf_path.exists()

    # PUBLIC METHODS

    def enable(self):
        """Enable the main configuration of the domain."""
        self.enabled_conf_path.symlink_to(self.conf_path)

    def disable(self):
        """Disable the main configuration of the domain."""
        self.enabled_conf_path.unlink()

    def generate_conf(self, template_name: str = None, **kwargs):
        """
        Overwrite the main configuration with the rendered configuration
        template for the domain.
        """
        if template_name:
            self.template_name = template_name
        try:
            template = self.get_template_environment().get_template(
                self.template_name
            )
        except TemplateNotFound:
            raise OSError(
                "Unable to find the template '%s' in %s."
                % (self.template_name, repr(self.templates_dir))
            )
        context = self.get_conf_context_data(**kwargs)
        self.conf_path.write_text(template.render(**context))

    def refresh_from_conf(self):
        """Retrieve properties from the main configuration of the domain."""
        self.update_properties_from_conf(self.conf_path.read_text())

    # OVERRIDABLE METHODS

    def get_template_environment(self, **kwargs) -> Environment:
        """Return the Jinja environment to use for template rendering."""
        options = {
            'loader': FileSystemLoader(self.templates_dir),
            'trim_blocks': True,
            'keep_trailing_newline': True,
        }
        options.update(kwargs)
        return Environment(**options)

    def get_conf_context_data(self, **kwargs) -> dict:
        """Return the template context for the domain's configuration."""
        kwargs.setdefault('domain', self)
        return kwargs

    def update_properties_from_conf(self, conf: str):
        """
        Retrieve and update the domain properties with values found in the
        given configuration.
        """
        self.template_name = self.get_property_from_conf(
            conf, 'template_name', r'.+'
        )

    def get_property_from_conf(
        self, conf: str, name: str, pattern=r'.*'
    ) -> str:
        """Retrieve a property's value from the given configuration."""
        match = re.search(
            r'^## %s=(%s)$' % (name, pattern), conf, re.MULTILINE
        )
        if match is None:
            raise ConfigurationError(
                "`%s` variable is not defined." % name, self.conf_path
            )
        return match.group(1)


class AlternativeServerNamesMixin:
    """
    Provide a way to define alternative server names of a domain.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._alternative_names = tuple()

    # PROPERTIES

    @property
    def alternative_names(self) -> tuple:
        """Return the alternative server names of the domain."""
        return self._alternative_names

    @alternative_names.setter
    def alternative_names(self, value: tuple):
        if not isinstance(value, tuple):
            raise ValueError(
                "Alternative server names must be given as a tuple."
            )
        self._alternative_names = value

    # DYNAMIC PROPERTIES

    @property
    def server_name(self) -> str:
        """The server name(s) of the domain."""
        return ' '.join([self.name] + list(self.alternative_names))


class DehydratedDomainMixin(AlternativeServerNamesMixin):
    """
    Provide a way to manage the domain's SSL/TLS certificates using dehydrated.
    """

    dehydrated_certs_dir = Path('/var/lib/dehydrated/certs')
    dehydrated_domains_path = Path('/etc/dehydrated/domains.txt')

    # DYNAMIC PROPERTIES

    @cached_property
    def certs_dir(self) -> Path:
        """The directory path to SSL/TLS certificates of the domain."""
        return self.dehydrated_certs_dir / self.name

    @property
    def has_certs(self) -> bool:
        """Whether SSL/TLS certificates of the domain exist."""
        return (self.certs_dir / 'privkey.pem').exists()

    # PUBLIC METHODS

    def generate_certs(self, stdout=None, stderr=subprocess.PIPE):
        """Generate the domain's SSL/TLS certificates using dehydrated."""
        subprocess.run(
            ['dehydrated', '--cron', '--domain', self.server_name],
            check=True,
            stdout=stdout,
            stderr=stderr,
        )

        self._update_dehydrated_domains()

    def enable(self):
        """
        Enable the main configuration of the domain and ensure that its server
        names are in the dehydrated domains' list.
        """
        super().enable()

        if self.has_https and self.has_certs:
            self._update_dehydrated_domains()

    def disable(self):
        """
        Disable the main configuration of the domain and ensure that its server
        names are not in the dehydrated domains' list.
        """
        super().disable()

        if self.has_certs:
            self._update_dehydrated_domains(remove=True)

    # INTERNAL METHODS

    def _update_dehydrated_domains(self, remove=False):
        """Update the dehydrated domains' list for the domain."""
        if not self.dehydrated_domains_path.is_file():
            if not remove:
                with open(self.dehydrated_domains_path, 'x') as f:
                    f.write('%s\n' % self.server_name)
            return

        domain_name_re = re.compile(r'(?:^|.+ ){}(?:$| .+)'.format(self.name))

        with open(self.dehydrated_domains_path, 'r') as f:
            lines = f.readlines()
        with open(self.dehydrated_domains_path, 'w') as f:
            is_domain_added = False

            for line in lines:
                if not domain_name_re.match(line.strip()):
                    f.write(line)
                elif not remove and not is_domain_added:
                    f.write('%s\n' % self.server_name)
                    is_domain_added = True

            if not remove and not is_domain_added:
                f.write('%s\n' % self.server_name)


# WEB DOMAIN CLASSES
# -----------------------------------------------------------------------------


class NGINXDomain(BaseDomain):
    """
    A Web domain intended to be served by NGINX.

    It is defined by one or more server names, and the protocol on which it
    must be available.
    """

    class Protocol(Enum):
        BOTH = 'both'
        HTTP = 'http'
        HTTPS = 'https'

    nginx_etc_dir = Path('/etc/nginx')
    nginx_log_dir = Path('/var/log/nginx')
    nginx_sites_available_dir = nginx_etc_dir / 'sites-available'
    nginx_sites_enabled_dir = nginx_etc_dir / 'sites-enabled'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._protocol = WebDomain.Protocol.BOTH

    # PROPERTIES

    @property
    def protocol(self) -> Protocol:
        """Return the `Protocol` on which the domain is available."""
        return self._protocol

    @protocol.setter
    def protocol(self, value: Protocol):
        if not isinstance(value, WebDomain.Protocol):
            raise ValueError(
                "Protocol must be a property of `WebDomain.Protocol`."
            )
        self._protocol = value

    # DYNAMIC PROPERTIES

    @cached_property
    def conf_path(self) -> Path:
        """The path to the NGINX configuration of the domain."""
        return self.nginx_sites_available_dir / self.name

    @cached_property
    def enabled_conf_path(self) -> Path:
        """The path to the enabled NGINX configuration of the domain."""
        return self.nginx_sites_enabled_dir / self.name

    @cached_property
    def local_conf_dir(self) -> Path:
        """The directory path to local NGINX configuration of the domain."""
        return self.nginx_sites_available_dir / '{}.d'.format(self.name)

    @cached_property
    def log_dir(self) -> Path:
        """The directory path to NGINX logs of the domain."""
        return self.nginx_log_dir / self.name

    @property
    def has_https(self) -> bool:
        """Whether the domain is available in HTTPS."""
        return self.protocol != WebDomain.Protocol.HTTP

    # OVERRIDABLE METHODS

    def get_conf_context_data(self, **kwargs) -> dict:
        if 'protocol' not in kwargs:
            kwargs['protocol'] = (
                WebDomain.Protocol.HTTP.value
                if not self.has_certs
                else self.protocol.value
            )
        return super().get_conf_context_data(**kwargs)

    def update_properties_from_conf(self, conf: str):
        super().update_properties_from_conf(conf)

        server_name = get_nginx_directive_value('server_name', conf).split(' ')
        if self.name not in server_name:
            raise ConfigurationError(
                "'{}' is not in `server_name {}` directive.".format(
                    self.name, server_name
                ),
                self.conf_path,
            )
        server_name.remove(self.name)
        self.alternative_names = tuple(server_name)

        protocol = self.get_property_from_conf(conf, 'protocol', r'[A-Z]+')
        try:
            self.protocol = WebDomain.Protocol[protocol]
        except KeyError:
            raise ConfigurationError(
                "'{}' is not a valid protocol.".format(protocol),
                self.conf_path,
            )


class WebDomain(DehydratedDomainMixin, NGINXDomain):
    """
    A Web domain intended to be served by NGINX with SSL/TLS certificates.

    It is defined by one or more server names, and the protocol on which it
    must be available. In case of HTTPS, its SSL/TLS certificates can be
    generated using dehydrated.
    """
