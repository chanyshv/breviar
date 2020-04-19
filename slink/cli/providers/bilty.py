import os.path as path
import json

import click

from ...core.providers import bitly
from ...core.utils import SERVICES
from ..text import BITLY_CONFIGURE_PROMPT
from ..constants import CONFIGS_PATH, BITLY_CONFIG_PATH
from ..utils import create_cli_config_files, get_config, ErrorHandlingGroup
from ..errors import NotConfigured


@click.group('bitly', cls=ErrorHandlingGroup)
def bitly_group(): pass


@bitly_group.command(help='Configure a service')
def configure():
    if not path.exists(CONFIGS_PATH):
        create_cli_config_files()
    access_token = click.prompt(BITLY_CONFIGURE_PROMPT)
    json.dump({
        'access_token': access_token,
    }, open(BITLY_CONFIG_PATH, 'w'))


@bitly_group.command(help='Shorten a link')
@click.argument('url')
def shorten(url: str):
    if not path.exists(BITLY_CONFIG_PATH):
        raise NotConfigured('bitly')
    config = get_config(BITLY_CONFIG_PATH, SERVICES.BITLY, {'access_token': {'type': 'string'}})
    shorten = bitly.BitlyProvider(config['access_token']).shorten_url(url)
    click.echo(shorten)
