import os.path as path
import json

import click

from ...core.utils import SERVICES
from ...core.providers import cuttly
from ..text import CUTTLY_CONFIGURE_PROMPT
from ..constants import CONFIGS_PATH, CUTTLY_CONFIG_PATH
from ..utils import create_cli_config_files, get_config, ErrorHandlingGroup
from ..errors import NotConfigured


@click.group('cuttly', cls=ErrorHandlingGroup)
def cuttly_group(): pass


@cuttly_group.command(help='Configure a service')
def configure():
    if not path.exists(CONFIGS_PATH):
        create_cli_config_files()
    access_token = click.prompt(CUTTLY_CONFIGURE_PROMPT)
    json.dump({
        'access_token': access_token,
    }, open(CUTTLY_CONFIG_PATH, 'w'))


@cuttly_group.command(help='Shorten a link')
@click.argument('url')
def shorten(url: str):
    if not path.exists(CUTTLY_CONFIG_PATH):
        raise NotConfigured('cuttly')
    config = get_config(CUTTLY_CONFIG_PATH, SERVICES.CUTTLY)
    shorten = cuttly.CuttlyProvider(config['access_token']).shorten(url)
    click.echo(shorten)
