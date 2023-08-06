# import subprocess
from .schemas import SiteConfigSchema  # SiteEnableSchema
from . import defaults
from . import utils

def default_cert_config():
    template = utils.get_template("default_certificat.j2")
    filename = defaults.NGINX_CONFIG_FOLDER / "@default.conf"
    with open(filename, "w") as f:
        f.write(template.render(config={}))


def from_site_enable_data(data):
    try:
        cfg = SiteConfigSchema.validate(data)
    except Exception:
        return None
    template = utils.get_template("site.j2")
    # print(f"got template {template}")
    filename = defaults.NGINX_CONFIG_FOLDER / (cfg["server_name"] + ".conf")
    with open(filename, "w") as f:
        f.write(template.render(config=cfg))
    return filename if filename.is_file() else None


def reload_nginx_conf(client):
    return utils.run_command(client, ["nginx", "-s", "reload"])
    # if defaults.NGINX_CONTAINER_NAME is None:
    #     process = subprocess.Popen(
    #         ["nginx", "-s", "reload"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    #     )
    #     stdout, stderr = process.communicate()
    #     return stdout, stderr
    # if isinstance(defaults.NGINX_CONTAINER_NAME, str):
    #     container = client.containers.get(defaults.NGINX_CONTAINER_NAME)

    #     stdout = container.exec_run(["nginx", "-s", "reload"]).output
    #     return stdout, ""
    # return "", ""


def generate_config(client, data, reload=True):
    cfg = from_site_enable_data(data)
    try:
        if cfg and reload:
            reload_nginx_conf(client)
        return cfg
    except Exception as e:
        raise Exception(f"""Error while trying to restart nginx: {e}""")
