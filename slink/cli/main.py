import operator as oper
import os.path as path
import json

import click

from slink.core import SERVICES
from ..core.providers import bitly
from .text import BITLY_CONFIGURE_PROMPT
from .constants import CONFIGS_PATH, BITLY_CONFIG_PATH
from .utils import create_cli_config_files, ErrorHandlingGroup, get_bitly_config
from .errors import NotConfigured


@click.group(cls=ErrorHandlingGroup)
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
        }, open(BITLY_CONFIG_PATH, 'w'))


@slink.command()
@click.argument('url')
@click.option('-S', '--service', default='bitly', show_default=True,
              type=click.Choice(list(map(oper.attrgetter('value'), SERVICES)))
              )
def shorten(url: str, service):
    if service == SERVICES.BITLY.value:
        if not path.exists(BITLY_CONFIG_PATH):
            raise NotConfigured(service)
        config = get_bitly_config()
        shorten = bitly.BitlyProvider(config['access_token']).shorten_url(url)
        click.echo(shorten)
