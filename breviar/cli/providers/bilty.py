import os.path as path
import json

import click

from ...core.providers import bitly
from ..text import BITLY_CONFIGURE_PROMPT
from ..constants import CONFIGS_PATH, BITLY_CONFIG_PATH
from ..utils import create_cli_config_files, get_bitly_config, ErrorHandlingGroup
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
def cut(url: str):
    if not path.exists(BITLY_CONFIG_PATH):
        raise NotConfigured('bitly')
    config = get_bitly_config()
    shorten = bitly.BitlyProvider(config['access_token']).shorten_url(url)
    click.echo(shorten)
