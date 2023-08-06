import click

from . import __version__
from .utils import get_remote_url, make_https_url, open_url, parse_remote_url


@click.command()
@click.version_option(version=__version__)
def main():
    """A Python CLI to open a web page from a Git repository."""
    remote_url = get_remote_url()
    # click.echo(remote_url)

    params = parse_remote_url(remote_url)
    # click.echo(params)

    url = make_https_url(params)

    message = f"{click.style('URL', bold=True)}: {url}"
    click.echo(message)

    open_url(url)
