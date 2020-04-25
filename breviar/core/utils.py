import enum

import click
import requests.exceptions

from ..core.errors import breviarError, NoResponse


class SERVICES(enum.Enum):
    BITLY = 'bitly'


class ErrorHandlingGroup(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except breviarError as e:
            click.echo(str(e))


def reraise_requests(f):
    def deco(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.ConnectTimeout as e:
            raise NoResponse from e

    return deco
