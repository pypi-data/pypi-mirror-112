# webdomains

Manage your Web domains served by NGINX.

## Installation
### Requirements

On a Debian-based host, you will need an already configured and running
[NGINX server](https://nginx.net/). You may also install the following
packages to satisfy the Python dependencies:
- `python3-click`
- `python3-jinja2`

To generate the SSL/TLS certificates for the domains, you will also have to
install and configure [dehydrated](https://dehydrated.io/). It is recommended
to use a recent version - i.e. from `buster-backports`. To serve the ACME
challenge, the default NGINX configuration of a domain is looking for
`/etc/nginx/snippets/acme-challenge.conf` - which can just contain:

```nginx
location /.well-known/acme-challenge {
    default_type "text/plain";
    alias        /var/lib/dehydrated/acme-challenges;
}
```

### Configuration

You can provide your own `server.conf` template which is used to generate the
NGINX configuration of a new domain. *webdomains* will look for a file with this
name in `/etc/webdomains/templates` at first. If it does not exist, the
[default template](webdomains/templates/server.conf) is used.

## Development

To set up a development environment, all you need to have to install is a
Python 3 interpreter, Git and Make. Then, run the following:

```bash
git clone https://forge.cliss21.org/cliss21/webdomains.git
cd webdomains/

# create and active a virtual environment
python3 -m venv venv/
source venv/bin/activate

# install the package with test requirements
pip install -e .[test]
```

You can now run the following commands:
- `make lint`: check the code syntax
- `make tests`: run the tests
- `make coverage`: report the code coverage

## License

*webdomains* is mainly developed by [Cliss XXI](https://www.cliss21.com) and
licensed under the [GPLv3+](LICENSE). Any contribution is welcome!
