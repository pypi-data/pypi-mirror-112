import sys

from dvenv.decorators import with_client
from dvenv.config import load_configuration
from dvenv.client import Client


@with_client
def python(client):
    args = sys.argv[1:]
    client.run_python(*args)


def interactive_python(config_path=None, **additional_cfg):
    cfg = load_configuration(path=config_path)
    cfg = {**cfg, **additional_cfg}
    client = Client(cfg=cfg, **additional_cfg)
    client.initialize_channel()
    client.run_python()


def run_notebook(config_path=None, **additional_cfg):
    cfg = load_configuration(path=config_path)
    cfg = {**cfg, **additional_cfg}
    client = Client(cfg=cfg, **additional_cfg)
    client.initialize_channel()
    client.run_python("-m", "jupyter", "notebook")
