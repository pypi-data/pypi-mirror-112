import argparse
from pathlib import Path
from . import utils
from . import defaults

parser = argparse.ArgumentParser(description='Nginx reverse proxy')
parser.add_argument(
    '-f', '--config_folder',
    default=utils.getenv("NGINX_CONFIG_FOLDER", defaults.NGINX_CONFIG_FOLDER),
    metavar='Config Foler',
    dest="folder",
    help=f"""
        Folder where to add nginx configs.
        By default, takes environment variable NGINX_CONFIG_FOLDER or { defaults.NGINX_CONFIG_FOLDER }
        if nginx run in a container, they must share the same folder
    """
)

parser.add_argument(
    '-c', '--container',
    default=utils.getenv("NGINX_CONTAINER_NAME", None),
    metavar='Nginx Container Name',
    dest="container",
    help='Container running nginx, by default, takes environment variable NGINX_CONTAINER_NAME or use local nginx'
)

parser.add_argument(
    '-d', '--domain',
    default=utils.getenv("URL_DOMAIN", defaults.URL_DOMAIN),
    metavar='Base Domain',
    dest="domain",
    help='Base domain to use. For a service "A" and domain "localhost", the service will be available under A.localhost'
)

def setup_defaults():
    args = parser.parse_args()
    defaults.URL_DOMAIN = args.domain
    defaults.NGINX_CONTAINER_NAME = args.container
    defaults.NGINX_CONFIG_FOLDER = Path(args.folder)
    if not defaults.NGINX_CONFIG_FOLDER.is_dir():
        raise Exception(f"Config Folder {args.folder} does not exists")
    # defaults.NGINX_CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)