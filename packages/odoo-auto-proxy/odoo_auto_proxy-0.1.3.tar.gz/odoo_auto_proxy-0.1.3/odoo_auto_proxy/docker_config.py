import json
from . import defaults
from . import utils

def get_env_dict(env_str):
    entries = (
        entry
        for entry in env_str.split("\n")
        if entry
    )
    env = {
        k: v
        for entry in entries
        for k,v in [entry.split("=")]
    }
    return env


def _container_ip(container):
    return container.attrs.get("NetworkSettings", {}).get("IPAddress")


def container_ip(container):
    ip = _container_ip(container)
    if not ip:
        utils.eprint("No ip found, adding container to bridge network")
        bridge = container.client.networks.get("bridge")
        bridge.connect(container.name)
        container.reload()
    return _container_ip(container)

def config_from_env(container):
    env_str = container.exec_run(["printenv"]).output.decode()
    env = get_env_dict(env_str)
    env["server_name"] = env["server_name"] + "." + defaults.URL_DOMAIN
    ip = container_ip(container)
    if ip:
        print(f"adding ip: {ip}")
        env["proxy_pass"] = ip + ":8069"
        env["web_upstream"] = env["proxy_pass"]
        env["poll_upstream"] = ip + ":8072"
    else:
        utils.eprint(f"No ip for container {container.name}")
        print(json.dumps(container.attrs, indent=4))
    return env