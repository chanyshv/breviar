import click

from .providers import cuttly_group, bitly_group
from .utils import ErrorHandlingGroup


@click.group(cls=ErrorHandlingGroup)
def slink(): pass


slink.add_command(bitly_group, 'bitly')
slink.add_command(cuttly_group, 'cuttly')
