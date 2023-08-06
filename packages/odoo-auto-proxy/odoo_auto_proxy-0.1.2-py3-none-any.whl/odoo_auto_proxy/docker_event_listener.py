import docker
import json

from . import args
from . import utils
from .docker_config import config_from_env
from .nginx import generate_config, reload_nginx_conf, default_cert_config
from . import certificate

def listener(client, handler):
    events = client.events()
    while True:
        e = events.next()
        if not isinstance(e, bytes):
            break
        e = json.loads(e.decode())
        handler(client, e)

def create_config(client, container, reload=True):
    config = config_from_env(container)
    try:
        cfg = generate_config(client, config, reload=reload)
        if cfg:
            print(f"config created at {str(cfg)}")
        return cfg
    except Exception as e:
        utils.eprint(f"Failed to create config for container: {e}")
        return None



def handler(client, e):
    if e.get("Type", "") != "container":
        return
    container_id = e.get("Actor", {}).get("ID")
    if not container_id:
        return
    try:
        action = e.get("Action", "")
        print(action)
        if action in ["start"]:
            ct = client.containers.get(container_id)
            create_config(client, ct)
    except Exception as e:
        utils.eprint(e)
    

def initialize_existing(client):
    for ct in client.containers.list():
        try:
            create_config(client, ct, reload=False)
        except Exception as e:
            utils.eprint(e)
    reload_nginx_conf(client)


def run():
    args.setup_defaults()
    client = docker.from_env()
    # default_cert_config()
    initialize_existing(client)
    # stdout, stderr = certificate.default_certificate(client)
    listener(client, handler)
    client.close()
