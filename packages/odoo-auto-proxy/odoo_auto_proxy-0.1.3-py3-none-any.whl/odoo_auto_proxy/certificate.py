
from . import utils
from . import defaults

# https://pypi.org/project/certbot-py/
# from certbot_py import client

# sudo certbot --authenticator standalone --installer nginx -d example.com --pre-hook “service nginx stop” --post-hook “service nginx start”

def create_certificate(client, domain, certname=None):
    certname = certname or domain.replace(".", "_")
    return utils.run_command(client, [
        "certbot", "certonly",
        "--server", defaults.DEFAULT_CERT_SERVER,
        "--webroot",  # Place files in a server's webroot folder for authentication
        "--webroot-path", defaults.DEFAULT_CERT_WEB_ROOT_PATH,
        "-d", domain,
        "--cert-name", certname
    ])

def default_certificate(client):
    # We must use manual plugin for wildcard
    domain = f"'*.{defaults.URL_DOMAIN}'"
    # return create_certificate(client, domain, defaults.DEFAULT_CERT_NAME)
    return utils.run_command(client, [
        "certbot", "certonly",
        "--server", defaults.DEFAULT_CERT_SERVER,
        "--manual",  # Obtain certificates interactively, or using shell script
        "-d", domain,
        "--cert-name", defaults.DEFAULT_CERT_NAME
    ])


def create_certificate(client, domain, certname=None):
    certname = certname or domain.replace(".", "_")
    return utils.run_command(client, [
        "certbot", "certonly",
        "--server", defaults.DEFAULT_CERT_SERVER,
        "--webroot",  # Place files in a server's webroot folder for authentication
        "--webroot-path", defaults.DEFAULT_CERT_WEB_ROOT_PATH,
        "-d", domain,
        "--cert-name", certname
    ])
    # use --nginx plugin (apt install python-certbot-nginx) instead of --webroot and --webroot-path?


def list_certificates(client):
    return utils.run_command(client, ["certbot", "certificates"])


def renew_certificates(client):
    return utils.run_command(client, ["certbot", "renew"])


def delete_certificate(client, domain, certname=None):
    certname = certname or domain.replace(".", "_")
    return utils.run_command(client, ["certbot", "delete", certname])
