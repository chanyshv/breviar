import os

from .constants import CONFIGS_PATH


def create_cli_config_files():
    os.mkdir(CONFIGS_PATH)
