import sys
from json import JSONDecodeError

import click
import requests
from requests import ConnectionError

from sotooncli.settings import SERVER_HOST

NON_JSON_RESPONSE_ERROR_MSG = "Invalid response, try updating your cache or try later"
ERROR_MSG_404 = "Not Found, try updating your cache"
CONNECTION_ERROR_MSG = "Cannot connect to server.\n\nYou might want to set \"SOTOON_SERVER_HOST\" to the right address."
UNKNOWN_ERROR = "unexpected error from server, please try again later"

METADATA_PATH = f"{SERVER_HOST}/api/v1/metadata"
EXEC_PATH = f"{SERVER_HOST}/api/v1/execute"


def get_metadata(path=""):
    url = f"{METADATA_PATH}/sotoon/{path}"
    try:
        res = requests.get(url=url)

        if res.status_code == 404:
            click.echo(ERROR_MSG_404)
            sys.exit(1)
        body = res.json()
        if res.status_code != 200 and body["type"] == 'error':
            click.echo(body["error"]["message"])
            sys.exit(1)
        return body
    except ConnectionError:
        click.echo(CONNECTION_ERROR_MSG)
        sys.exit(1)
    except JSONDecodeError:
        click.echo(NON_JSON_RESPONSE_ERROR_MSG)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        click.echo(e)
        sys.exit(1)


def execute(path, params):
    body = {"path": ["sotoon"] + path, "args": params}
    return send_request_from_cli("post", EXEC_PATH, body)


def send_request_from_cli(method, url, body):
    try:
        res = requests.request(method=method, url=url, json=body)
        if res.status_code == 404:  # TODO 404 response is not json
            raise click.ClickException(ERROR_MSG_404)
        body = res.json()
        if res.status_code != 200 and body["type"] == 'error':
            raise click.ClickException(body["error"]["message"])
        return body
    except ConnectionError:
        raise click.ClickException(CONNECTION_ERROR_MSG)
    except JSONDecodeError:
        raise click.ClickException(NON_JSON_RESPONSE_ERROR_MSG)
    except KeyError:
        raise click.ClickException(UNKNOWN_ERROR)
