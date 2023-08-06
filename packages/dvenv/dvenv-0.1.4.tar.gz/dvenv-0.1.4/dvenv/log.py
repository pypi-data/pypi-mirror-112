import click
import sys
import os

OUTPUT_PREFIX = "dvenv: "


def warn(str):
    click.echo(
        f"{click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(str, bg='black', fg='red')}"  # noqa
    )


def debug(str):
    if int(os.getenv("DVENV_DEBUG", 0)) != 0:
        click.echo(
            f"DEBUG: {click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(str, bg='black', fg='white')}"  # noqa
        )


def die(str):
    click.echo(
        f"{click.style(OUTPUT_PREFIX, bg='black', fg='white')}FATAL: {click.style(str, bg='black', fg='red')}"  # noqa
    )
    sys.exit(1)


def info(str):
    click.echo(
        f"{click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(str, bg='black', fg='white')}"  # noqa
    )


def action(str, prepend=""):
    click.echo(
        f"{prepend}{click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(str, bg='black', fg='yellow')}"  # noqa
    )


def warn_confirm(str):
    return click.confirm(
        f"{click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(str, bg='black', fg='red')}",  # noqa
    )


def action_confirm(_str):
    return click.confirm(
        f"{click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(_str, bg='black', fg='yellow')}",  # noqa
    )


def action_prompt(str, type, default=""):
    return click.prompt(
        f"{click.style(OUTPUT_PREFIX, bg='black', fg='white')}{click.style(str, bg='black', fg='yellow')}",  # noqa
        type=type,
        show_default=True,
        default=default,
    )
