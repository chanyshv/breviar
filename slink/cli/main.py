import click

from .providers import bilty_group
from .utils import ErrorHandlingGroup


@click.group(cls=ErrorHandlingGroup)
def slink(): pass


slink.add_command(bilty_group, 'bitly')
