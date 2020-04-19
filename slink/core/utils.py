import enum

import click
import requests.exceptions

from slink.core.errors import SLinkError, NoResponse, NoEthernetConnection


class SERVICES(enum.Enum):
    BITLY = 'bitly'
    CUTTLY = 'cuttly'


class ErrorHandlingGroup(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except SLinkError as e:
            click.echo(str(e))


def reraise_requests(f):
    def deco(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.ConnectTimeout as e:
            raise NoResponse from e
        except requests.exceptions.ConnectionError as e:
            raise NoEthernetConnection from e

    return deco
