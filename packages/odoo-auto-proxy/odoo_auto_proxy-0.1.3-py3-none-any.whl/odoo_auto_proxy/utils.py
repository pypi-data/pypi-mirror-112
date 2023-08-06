import os
import sys
import subprocess
from jinja2 import Environment, FileSystemLoader, PackageLoader, ChoiceLoader

def eprint(*args, **kwargs):
    file = kwargs.pop("file", sys.stderr)
    print(*args, file=file, **kwargs)


_sentinelle = object()

def getenv(key, default=_sentinelle):
    if key not in os.environ:
        if default is _sentinelle:
            raise Exception("No environment variable {key}".format(
                key=key,
            ))
        return default
    return os.environ[key]
    

def run_command(client, command):
    print("Command: ", " ".join(command))
    if defaults.NGINX_CONTAINER_NAME is None:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        return stdout, stderr
    if isinstance(defaults.NGINX_CONTAINER_NAME, str):
        container = client.containers.get(defaults.NGINX_CONTAINER_NAME)

        stdout = container.exec_run(command).output
        return stdout, ""
    return "", ""



from . import defaults
def get_template(name):
    LOADER = ChoiceLoader([
        PackageLoader('odoo_auto_proxy', 'templates'),
        FileSystemLoader(str(defaults.TEMPLATES_FOLDER_PATH))
    ])


    env = Environment(loader=LOADER)
    return env.get_template(name)
