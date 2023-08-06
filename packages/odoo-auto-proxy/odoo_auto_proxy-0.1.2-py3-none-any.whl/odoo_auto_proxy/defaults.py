import os
from pathlib import Path
from . import utils

ROOT_PATH = Path(os.path.dirname(os.path.realpath(__file__))).resolve()
TEMPLATES_FOLDER_NAME = "templates"
TEMPLATES_FOLDER_PATH = ROOT_PATH.joinpath(TEMPLATES_FOLDER_NAME).resolve()

URL_DOMAIN = "localhost"
NGINX_CONTAINER_NAME = utils.getenv("NGINX_CONTAINER_NAME", None)
NGINX_CONFIG_FOLDER = "/etc/nginx/conf.d"
DEFAULT_CERT_NAME = "default"
DEFAULT_CERT_SERVER = "https://acme-v02.api.letsencrypt.org/directory"
DEFAULT_CERT_WEB_ROOT_PATH = "/var/www/letsencrypt"
# NGINX_CONFIG_FOLDER.mkdir(parents=True, exist_ok=True)