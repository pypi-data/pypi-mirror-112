import click

from dvenv import log
from dvenv.server import Server
from dvenv.decorators import with_config


@click.command()
@with_config
def host(cfg):
    """Host a dvenv environment for clients."""

    server = Server(cfg=cfg)
    server.run()
