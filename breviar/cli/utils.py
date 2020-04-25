import os
import sys

import click
import json
import cerberus

from breviar.core.errors import breviarError
from breviar.core.utils import SERVICES
from .constants import CONFIGS_PATH, BITLY_CONFIG_PATH
from .errors import ConfigNotValid


def create_cli_config_files():
    os.mkdir(CONFIGS_PATH)


def get_bitly_config():
    try:
        config = json.load(open(BITLY_CONFIG_PATH))
    except json.JSONDecodeError as e:
        raise ConfigNotValid(SERVICES.BITLY.value) from e
    schema = {'access_token': {'type': 'string'}}
    is_valid = cerberus.Validator(schema).validate(config)
    if not is_valid:
        raise ConfigNotValid(SERVICES.BITLY.value)
    return config


class ErrorHandlingGroup(click.Group):
    def __call__(self, *args, **kwargs):
        try:
            return self.main(*args, **kwargs)
        except breviarError as e:
            click.echo(str(e))
            sys.exit(1)
