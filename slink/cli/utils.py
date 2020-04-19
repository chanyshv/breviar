import os
import sys

import click
import json
import cerberus

from slink.core.errors import SLinkError
from slink.core.utils import SERVICES
from .constants import CONFIGS_PATH, BITLY_CONFIG_PATH
from .errors import ConfigNotValid


def create_cli_config_files():
    os.mkdir(CONFIGS_PATH)


def get_config(path: str, service: SERVICES, validation_schema: dict = None):
    try:
        config = json.load(open(path))
    except json.JSONDecodeError as e:
        raise ConfigNotValid(service.value) from e
    if validation_schema:
        is_valid = cerberus.Validator(validation_schema).validate(config)
        if not is_valid:
            raise ConfigNotValid(SERVICES.BITLY.value)
    return config


class ErrorHandlingGroup(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except SLinkError as e:
            click.echo(str(e))
            sys.exit(1)
