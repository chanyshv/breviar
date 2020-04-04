import operator as oper
import os.path as path
import json

import click

from slink.core import bitly, SERVICES
from .text import BITLY_CONFIGURE_PROMPT
from .constants import CONFIGS_PATH
from .utils import create_cli_config_files


@click.group()
@click.pass_context
def slink(ctx: click.Context): pass


@slink.command()
@click.option('-S', '--service', default='bitly', show_default=True,
              type=click.Choice(list(map(oper.attrgetter('value'), SERVICES)))
              )
def configure(service):
    if not path.exists(CONFIGS_PATH):
        create_cli_config_files()
    if service == SERVICES.BITLY.value:
        access_token = click.prompt(BITLY_CONFIGURE_PROMPT)
        json.dump({
            'access_token': access_token,
        }, open(path.join(CONFIGS_PATH, 'bitly_config.json'), 'w'))


@slink.command()
@click.argument('url')
@click.option('-S', '--service', default='bitly', show_default=True,
              type=click.Choice(list(map(oper.attrgetter('value'), SERVICES)))
              )
def shorten(url: str, service):
    if service == 'bitly':
        shorten = bitly.BitlyClient().shorten_url(url)
        click.echo(shorten)
