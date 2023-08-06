import click

from dvenv import log
from dvenv.decorators import with_client


@click.command()
@with_client
def init(client):
    """Initialize a new dvenv environment."""

    return_code = client.create_new_environment(
        python_version="python3.8", path="/tmp/test2"
    )

    if return_code == 0:
        log.action("Created new virtual environment")
    else:
        log.die(f"Could not create a new environment, return code: {return_code}")
