import click

from sotooncli.cache_utils import CacheUtils


@click.group()
def cache():
    """manages cache"""


@cache.command()
def update():
    """updates cache and exits"""
    CacheUtils().update_cache()
    click.echo("Cache updated successfully.")


@cache.command()
def remove():
    """removes existing cache"""
    CacheUtils().remove_cache()
    click.echo("Cache removed successfully.")
