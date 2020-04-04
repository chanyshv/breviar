import click
from slink.core import bitly


@click.command()
@click.argument('url',)
def slink(url: str):
    shorten = bitly.BitlyClient().shorten_url(url)
    click.echo(shorten)
    # click.echo(f'i got your url.\nURL: "{url}"')
