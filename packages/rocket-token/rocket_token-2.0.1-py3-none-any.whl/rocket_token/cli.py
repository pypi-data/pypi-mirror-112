"""Module to hold all of the command line utilities that
RocketTokens provides
"""

import os
import sys
from typing import NoReturn, Union

import click

from .token import RocketToken


@click.command()
@click.argument("directory")
def generate_keys(directory):
    """Generate public and private keys and save them to `directory`

    Args:
        DIRECTORY (str): The directory to save the public and private keys in.\n
    """
    RocketToken.generate_key_pair(directory)
    click.echo(f"Key-pair saved to `{directory}`")


@click.command()
@click.argument("public_key", type=click.Path(exists=True))
@click.argument("path")
@click.argument("method")
@click.argument("exp", type=int)
@click.option("--payload", "-p", multiple=True)
def generate_web_token(
    public_key: str, path: str, method: str, exp: int, payload: list
) -> Union[NoReturn, None]:
    """Generate a web token for use within REST APIs.

    Args:
        PATH (str): The path/endpoint the token is valid for.\n
        METHOD (str): The HTTP method the token is valid for.\n
        EXP (int): The number of minutes until the token expires.\n
        PAYLOAD (str): Space seperated key-value arguments of the form name=Jon\n
    """
    for p in payload:
        if "=" not in p:
            click.echo("Payload must be a key value pair of the format i.e key=value")
            sys.exit(1)
    payload_values = {p.split("=")[0]: p.split("=")[1] for p in payload}

    rt = RocketToken.load_keys_from_path(public_path=public_key)
    token = rt.generate_web_token(path=path, exp=exp, method=method, **payload_values)
    click.echo(token)


@click.command()
@click.argument("path")
@click.argument("method")
@click.argument("exp", type=int)
@click.option("--payload", "-p", multiple=True)
def generate_developer_web_token(
    path: str, method: str, exp: int, payload: list
) -> Union[NoReturn, None]:
    """Generate a developer web token for use within REST apis.

    PATH (str): The path/endpoint the token is valid for.\n
    METHOD (str): The HTTP method the token is valid for.\n
    EXP (int): The number of minutes until the token expires.\n
    PAYLOAD (str): Space seperated key-value arguments of the form name=Jon\n
    """
    for p in payload:
        if "=" not in p:
            click.echo("Payload must be a key value pair of the format i.e key=value")
            sys.exit(1)
    payload_values = {p.split("=")[0]: p.split("=")[1] for p in payload}

    os.environ["ROCKET_DEVELOPER_MODE"] = "true"
    rt = RocketToken()
    token = rt.generate_web_token(path=path, exp=exp, method=method, **payload_values)
    click.echo(token)
