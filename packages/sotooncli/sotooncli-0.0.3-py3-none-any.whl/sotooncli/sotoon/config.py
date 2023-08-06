import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

import click
import yaml

from sotooncli.settings import APP_NAME
from sotooncli.utils import read_yaml_file, write_to_yaml, delete_file, get_strerror

APP_CONFIG_NAME = "app_config.yaml"
APP_DIR = click.get_app_dir(app_name=APP_NAME)
USER_CONFIG_DIR_NAME = "configurations"
USER_DEFAULT_CONFIG_NAME = "config_default.yaml"
ACTIVE_CONFIG = "active_config"


@click.group()
def config():
    """view and edit configs."""
    if not os.path.exists(f"{APP_DIR}/{USER_CONFIG_DIR_NAME}") or not os.path.isfile(
            f"{APP_DIR}/{APP_CONFIG_NAME}"):
        dirs = [APP_DIR, f"{APP_DIR}/{USER_CONFIG_DIR_NAME}"]
        files = [APP_CONFIG_NAME, f"{USER_CONFIG_DIR_NAME}/{USER_DEFAULT_CONFIG_NAME}"]
        default_config = {ACTIVE_CONFIG: USER_DEFAULT_CONFIG_NAME}
        for directory in dirs:
            os.makedirs(directory, exist_ok=True)
        for file_path in files:
            file = Path(f"{APP_DIR}/{file_path}")
            file.touch(exist_ok=True)
        with open(f"{APP_DIR}/{APP_CONFIG_NAME}", mode='w') as config_file:
            yaml.dump(default_config, config_file)


@config.command()
@click.argument("key", metavar="KEY", required=True)
def get(key):
    """get the key's value from the active config

    \b\bArguments:

    KEY  This parameter is required.
    """
    active_config = get_active_config_name()
    config_data = read_user_config(active_config)
    if key not in config_data:
        raise click.BadParameter("No such property is set in the active config")
    click.echo(config_data[key])


@config.command()
def list():
    """get active config's values"""
    active_config = get_active_config_name()
    config_data = read_user_config(active_config)
    click.echo(config_data)


@config.command()
@click.argument("key", metavar="KEY", required=True)
@click.argument("value", metavar="VALUE", required=True)
def set(key, value):
    """set the value to key in the active config.

    \b\bArguments:


    KEY    This parameter is required.

    VALUE  This parameter is required.
    """
    active_config = get_active_config_name()
    config_data = read_user_config(active_config) or {}
    config_data[key] = value
    write_to_user_config(active_config, config_data)
    click.echo(f"Set {key} to {value}")


@config.command()
@click.argument("key", metavar="KEY", required=True)
def unset(key):
    """unset the value to key in the active config.

    \b\bArguments:


    KEY  This parameter is required.
    """
    active_config = get_active_config_name()
    config_data = read_user_config(active_config)
    if key not in config_data:
        raise click.BadParameter(f"No such property \"{key}\" is set in the active config.")
    config_data.pop(key)
    write_to_user_config(active_config, config_data)
    click.echo(f"Unset {key}")


@config.group()
def configurations():
    """Manages the set of named configurations"""


@configurations.command()
@click.argument("name", metavar="CONFIG_NAME", required=True)
def create(name):
    """Creates a new named configuration.

    \b\bArguments:


    CONFIG_NAME  This parameter is required.
    """
    path = f"{APP_DIR}/{USER_CONFIG_DIR_NAME}/{name}.yaml"
    file = Path(path)
    if file.is_file():
        raise click.BadParameter(f"A configuration with name \"{name}\" already exists.")
    file.touch()
    click.echo(f"Created {name} config.")


@configurations.command()
@click.argument("name", metavar="CONFIG_NAME", required=True)
def delete(name):
    """Deletes a named configuration.

    \b\bArguments:


    CONFIG_NAME  This parameter is required.
    """
    path = f"{APP_DIR}/{USER_CONFIG_DIR_NAME}/{name}.yaml"
    try:
        delete_file(path)
    except FileNotFoundError:
        raise click.BadParameter("No such config.")
    except Exception as e:
        raise click.BadParameter(f"Could not delete Config: {get_strerror(e)}")
    click.echo(f"Deleted {name} config.")


@configurations.command()
@click.argument("name", metavar="CONFIG_NAME", required=True)
def activate(name):
    """Activates an existing named configuration.

    \b\bArguments:

    CONFIG_NAME  This parameter is required.
    """
    user_config_path = f"{APP_DIR}/{USER_CONFIG_DIR_NAME}/{name}.yaml"
    if not os.path.isfile(user_config_path):
        raise click.BadParameter("No such config.")
    app_config_path = f"{APP_DIR}/{APP_CONFIG_NAME}"
    config_data = read_yaml_file(app_config_path) or {}
    config_data[ACTIVE_CONFIG] = f"{name}.yaml"
    write_to_yaml(app_config_path, config_data)
    click.echo(f"Set active config to {name}")


@configurations.command()
@click.argument("name", metavar="CONFIG_NAME", required=True)
def describe(name):
    """Describes a named configuration by listing its key-value.

    \b\bArguments:

    CONFIG_NAME  This parameter is required.
    """
    config_data = read_user_config(f"{name}.yaml")
    click.echo(config_data)


@configurations.command()
def list():
    """Lists existing named configurations."""
    path = f"{APP_DIR}/{USER_CONFIG_DIR_NAME}"
    files = [os.path.splitext(f)[0] for f in listdir(path) if isfile(join(path, f))]
    click.echo(files)


def get_active_config_name():
    app_config_path = f"{APP_DIR}/{APP_CONFIG_NAME}"
    if not isfile(app_config_path):
        raise click.UsageError(message=f"App config is not found in {app_config_path}")
    config_data = read_yaml_file(app_config_path)
    if ACTIVE_CONFIG not in config_data:
        raise click.UsageError(message="No active config found")
    return config_data[ACTIVE_CONFIG]


def get_active_config_path():
    return f"{APP_DIR}/{USER_CONFIG_DIR_NAME}/{get_active_config_name()}"


def read_user_config(name):
    config_path = f"{APP_DIR}/{USER_CONFIG_DIR_NAME}/{name}"
    config_data = read_yaml_file(config_path)
    return config_data


def write_to_user_config(name, value):
    config_path = f"{APP_DIR}/{USER_CONFIG_DIR_NAME}/{name}"
    write_to_yaml(config_path, value)
