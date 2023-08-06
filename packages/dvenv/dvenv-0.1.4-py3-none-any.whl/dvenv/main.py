import click
import sys

from dvenv.commands import host
from dvenv.commands import init


@click.group()
def entry_point():
    pass


def main():
    entry_point.add_command(host.host)
    entry_point.add_command(init.init)
    entry_point()


if __name__ == "__main__":
    sys.exit(main())
