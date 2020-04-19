import os.path as path
import json
import typing as ty

import click
from tabulate import tabulate

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


@cuttly_group.command(help='Get shorten link stats')
@click.argument('urls', nargs=-1)
@click.option('--title', '-t', default=True, is_flag=True, help='Show title')
@click.option('--clicks', '-c', default=True, is_flag=True, help='Show clicks')
@click.option('--short_link', '-s', default=True, is_flag=True, help='Show short link')
@click.option('--full_link', '-f', default=False, is_flag=True, help='Show full link')
@click.option('--date', '-d', default=False, is_flag=True, help='Show date')
@click.option('--stats_link', '-S', default=True, is_flag=True, help='Show stats link')
def stats(urls: ty.Sequence[str],
          title: bool,
          clicks: bool,
          short_link: bool,
          full_link: bool,
          date: bool,
          stats_link: bool,
          ):
    if not path.exists(CUTTLY_CONFIG_PATH):
        raise NotConfigured('cuttly')
    config = get_config(CUTTLY_CONFIG_PATH, SERVICES.CUTTLY)
    stats_headers = {
        'title': (title, 'title'),
        'clicks': (clicks, 'clicks'),
        'short link': (short_link, 'short_link'),
        'full link': (full_link, 'full_link'),
        'date': (date, 'date'),
        'stats link': (stats_link, 'stats_link'),
    }
    stats_headers = {k: i for k, i in stats_headers.items() if i[0]}
    stats = []
    for url in urls:
        raw_stats = cuttly.CuttlyProvider(config['access_token']).stats(url)
        url_stats = []
        for item in stats_headers.values():
            url_stats.append(raw_stats[item[1]])
        stats.append(url_stats)
    click.echo(tabulate(stats, headers=list(stats_headers.keys())))
