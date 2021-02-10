"""Command line interface definition."""

import click
from mkdocs_newsletter import version
from mkdocs_newsletter.entrypoints import (
    load_config,
    load_logger,
)


@click.group()
@click.version_option(version="", message=version.version_info())
@click.option("-v", "--verbose", is_flag=True)
def cli(verbose: bool) -> None:
    """Command line interface main click entrypoint."""

    load_logger(verbose)


@cli.command(hidden=True)
def null() -> None:
    """Do nothing.

    Used for the tests until we have a better solution.
    """


if __name__ == "__main__":  # pragma: no cover
    # E1120: As the arguments are passed through the function decorators instead of
    # during the function call, pylint get's confused.
    cli(ctx={})  # noqa: E1120
