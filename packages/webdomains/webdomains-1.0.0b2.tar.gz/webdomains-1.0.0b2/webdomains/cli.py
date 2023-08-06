import logging
import os
import subprocess
from functools import update_wrapper
from shutil import rmtree

import click
from click.exceptions import Exit

from webdomains import __version__
from webdomains.core import ConfigurationError, WebDomain, reload_nginx
from webdomains.utils import LogPipe, setup_click_logger

logger = setup_click_logger(logging.getLogger(__name__))
logger.setLevel(logging.DEBUG)
logger.propagate = False


# HELPERS
# -----------------------------------------------------------------------------


def die(message: str, code: int = 1):
    """Print an error message and exit."""
    logger.critical(message)
    raise Exit(code)


def mkdir(path: str, **kwargs):
    """Create the directory `path` or change its mode if it exists."""
    if not os.path.isdir(path):
        logger.info("Creating directory '%s'…", path)
        os.mkdir(path, **kwargs)
    elif 'mode' in kwargs:
        logger.info("Changing mode of '%s'…", path)
        os.chmod(path, kwargs['mode'])


def reload_nginx_or_die(callback=None):
    """
    Try to reload the NGINX server and die if an error occurs - after calling
    the `callback` method.
    """
    try:
        logger.info("Reloading NGINX server…")
        reload_nginx()
    except subprocess.SubprocessError as e:
        if callable(callback):
            callback()
        die(str(e))


# COMMANDS
# -----------------------------------------------------------------------------


def domain_argument(f):
    """Add a `domain` argument which will be passed as `WebDomain` object."""

    @click.argument('domain', metavar='DOMAIN_NAME')
    def new_func(domain, *args, **kwargs):
        if not isinstance(domain, WebDomain):
            domain = WebDomain(domain)
        return f(domain, *args, **kwargs)

    return update_wrapper(new_func, f)


@click.group()
@click.option(
    '-q', '--quiet', is_flag=True, help="Suppress non-error messages."
)
@click.version_option(version=__version__, message='%(version)s')
def cli(quiet: bool = False):
    """Manage Web domains served by this host."""
    if quiet:
        logger.setLevel(logging.ERROR)


@cli.command(name='list')
@click.option(
    '-e/-d',
    '--enabled/--disabled',
    default=None,
    help="List enabled or disabled domains only.",
)
def list_webdomains(enabled: bool = None):
    """List existing domains."""
    if enabled is True:

        def _handle_domain(domain):
            if domain.is_enabled:
                click.echo(domain)

    elif enabled is False:

        def _handle_domain(domain):
            if not domain.is_enabled:
                click.echo(domain)

    else:

        def _handle_domain(domain):
            if domain.is_enabled:
                click.echo(domain)
            else:
                click.echo("{} (disabled)".format(domain))

    with os.scandir(WebDomain.nginx_sites_available_dir) as it:
        for entry in it:
            if entry.is_file() and not (
                entry.name.startswith('.') or entry.name == 'default'
            ):
                _handle_domain(WebDomain(entry.name))


@cli.command(name='info', short_help="Show domain informations.")
@domain_argument
def info_webdomain(domain: WebDomain):
    """Show informations about the domain DOMAIN_NAME."""
    if not domain.exists:
        die("Domain does not exist.")

    try:
        domain.refresh_from_conf()
    except ConfigurationError as e:
        logger.warning(str(e))
        die("Unable to load the domain's NGINX configuration.")

    click.echo("enabled: {}".format("yes" if domain.is_enabled else "no"))
    click.echo("server_name: {}".format(domain.server_name))
    click.echo("protocol: {}".format(domain.protocol.value))

    if domain.has_https:
        click.echo("certs: {}".format("yes" if domain.has_certs else "no"))

    click.echo("template_name: {}".format(domain.template_name))


@cli.command(name='add', short_help="Add a domain.")
@click.option(
    '-n',
    '--alternative-name',
    multiple=True,
    metavar="DOMAIN_NAME",
    help="Alternative server name (can be provided multiple times).",
)
@click.option(
    '-h', '--http-only', is_flag=True, help="Do not serve over HTTPS."
)
@click.option(
    '-s', '--https-only', is_flag=True, help="Redirect HTTP to HTTPS."
)
@click.option(
    '-e', '--enable', is_flag=True, help="Enable the created domain."
)
@click.option(
    '-f', '--force', is_flag=True, help="Overwrite existing configuration."
)
@click.option(
    '-t', '--template-name', metavar="NAME", help="The template name to use."
)
@domain_argument
@click.pass_context
def add_webdomain(
    ctx: click.Context,
    domain: WebDomain,
    alternative_name: tuple = None,
    http_only: bool = False,
    https_only: bool = False,
    enable: bool = False,
    force: bool = False,
    template_name: str = None,
):
    """
    Create the NGINX configuration and directories for the domain DOMAIN_NAME.

    DOMAIN_NAME will be the principal server name used for all other commands.
    It is possible to provide alternative server names for the domain with
    `--alternative-name`.

    By default, the domain will be served over HTTP and HTTPS. It is possible
    to restrict the protocol with `--http-only` or `--https-only`. Note that if
    the SSL/TLS certificates of the domain does not exist yet, the domain will
    be served over HTTP only at first. They will be automatically generated
    using dehydrated when the domain is enabled.
    """
    if alternative_name:
        domain.alternative_names = tuple(alternative_name)

    if http_only and https_only:
        raise click.UsageError(
            "--http-only and --https-only are not compatible.", ctx
        )
    elif http_only:
        domain.protocol = WebDomain.Protocol.HTTP
    elif https_only:
        domain.protocol = WebDomain.Protocol.HTTPS

    if domain.exists:
        if not force:
            die(
                "Domain already exists. "
                "Use --force if you want to regenerate its configuration."
            )
        logger.warning("NGINX configuration will be overwritten.")

    try:
        logger.info("Generating NGINX configuration…")
        domain.generate_conf(template_name)
    except OSError as e:
        die(str(e))

    mkdir(domain.local_conf_dir, mode=0o755)
    mkdir(domain.log_dir, mode=0o750)

    if enable:
        ctx.invoke(enable_webdomain, domain=domain)


@cli.command(name='remove', short_help="Remove a domain.")
@click.option(
    '-c', '--clean', is_flag=True, help="Delete all associated directories."
)
@click.option(
    '-f', '--force', is_flag=True, help="Remove even if the domain is enabled."
)
@domain_argument
@click.pass_context
def remove_webdomain(
    ctx: click.Context,
    domain: WebDomain,
    clean: bool = False,
    force: bool = False,
):
    """
    Remove the NGINX configuration of the domain DOMAIN_NAME.

    If `--clean` is given, the local NGINX configuration and logs of the domain
    will also be deleted.
    """
    if domain.is_enabled:
        if not force:
            die(
                "Domain is currently enabled. "
                "Use --force if you want to remove it nevertheless."
            )
        ctx.invoke(disable_webdomain, domain=domain)

    if domain.exists:
        logger.info("Deleting NGINX configuration…")
        domain.conf_path.unlink()
    else:
        logger.debug("The NGINX configuration does not exist.")

    if clean:
        for path in (domain.local_conf_dir, domain.log_dir):
            if os.path.isdir(path):
                logger.info("Deleting directory « %s »…", path)
                rmtree(path)


@cli.command(name='enable', short_help="Enable a domain.")
@domain_argument
def enable_webdomain(domain: WebDomain):
    """
    Enable the NGINX configuration of the domain DOMAIN_NAME and generate as
    needed its SSL/TLS certificates.
    """
    if not domain.exists:
        die("Domain does not exist.")

    try:
        domain.refresh_from_conf()
    except ConfigurationError as e:
        logger.warning(str(e))
        logger.die("Domain's NGINX configuration could not be loaded.")

    need_certs_generation = domain.has_https and not domain.has_certs

    if domain.is_enabled:
        logger.debug("Domain's NGINX configuration is already enabled.")

        if not need_certs_generation:
            return
    else:
        logger.info("Enabling domain's NGINX configuration…")
        domain.enable()

        reload_nginx_or_die(domain.disable)

    if need_certs_generation:
        try:
            logger.info("Generating SSL/TLS certificates for the domain…")
            with LogPipe(logging.DEBUG, logger=logger) as stdout:
                domain.generate_certs(stdout=stdout)
        except subprocess.CalledProcessError as e:
            die(
                "Unable to generate SSL/TLS certificates:\n{}".format(
                    e.stderr.decode().strip()
                )
            )

        logger.info("Regenerating NGINX configuration…")
        domain.generate_conf()

        reload_nginx_or_die(domain.disable)


@cli.command(name='disable', short_help="Disable a domain.")
@domain_argument
def disable_webdomain(domain: WebDomain):
    """Disable the NGINX configuration of the domain DOMAIN_NAME."""
    if not domain.exists:
        die("Domain does not exist.")

    if not domain.is_enabled:
        logger.debug("Domain's NGINX configuration is already disabled.")
        return

    logger.info("Disabling domain's NGINX configuration…")
    domain.disable()

    try:
        logger.info("Reloading NGINX server…")
        reload_nginx()
    except subprocess.SubprocessError as e:
        logger.warning(str(e))


if __name__ == '__main__':  # pragma: no cover
    cli()
