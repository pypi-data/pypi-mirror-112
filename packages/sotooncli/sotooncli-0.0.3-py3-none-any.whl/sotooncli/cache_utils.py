from datetime import date, timedelta, datetime

import click

from sotooncli import requests
from sotooncli.sotoon.config import APP_DIR
from sotooncli.utils import delete_file, write_to_json, read_json, get_strerror


class CacheUtils:
    _instance = None
    DATE_KEY = "date"
    DATA_KEY = "result"

    def __new__(cls, use_cache=True):
        if cls._instance is None:
            cls._instance = super(CacheUtils, cls).__new__(cls)
            cls._instance.path = f"{APP_DIR}/cache.json"
            cls._instance.duration = timedelta(days=5)
            cls._instance.data = None
            cls._instance.date = None
            cls._instance.use_cache = use_cache
        return cls._instance

    def read_cache(self):
        if not self._instance.use_cache:
            return False
        try:
            data = read_json(self.path)
            self._instance.data = data[self.DATA_KEY]
            self._instance.date = datetime.fromisoformat(data[self.DATE_KEY]).date()
            return True
        except KeyError:
            click.echo("Warning: Cache file is invalid")
        except FileNotFoundError:
            return False
        except Exception as e:
            click.echo(f"Warning: could not read cache: {get_strerror(e)}")
        return False

    def update_cache(self):
        self._instance.data = requests.get_metadata()
        self._instance.date = date.today()
        if not self._instance.use_cache:
            return
        cache = {
            self.DATA_KEY: self._instance.data,
            self.DATE_KEY: self._instance.date.isoformat()
        }
        write_to_json(path=self._instance.path, value=cache)

    def has_expired(self):
        if self._instance.date + self._instance.duration <= date.today():
            return True
        return False

    def get_cache(self):
        successful = self.read_cache()
        if successful and self.has_expired():
            successful = False
        if not successful:
            self.update_cache()
        return self._instance.data

    def remove_cache(self):
        try:
            delete_file(self._instance.path)
        except FileNotFoundError:
            return
        except Exception:
            raise click.ClickException("Could not delete cache.")
