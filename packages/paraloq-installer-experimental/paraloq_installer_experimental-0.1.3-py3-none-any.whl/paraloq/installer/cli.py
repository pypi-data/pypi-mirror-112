import click
import requests
import json
import os
import datetime
import re

from cookiecutter.main import cookiecutter

from paraloq.installer import session
from paraloq.installer.prompt import ParaloqConfig


def _login(verbose: bool = True):

    paraloq_file = ParaloqConfig.from_disc()
    now = datetime.datetime.now().timestamp()
    valid_token = (float(paraloq_file.cached_bearer.get("expires_at", 0)) - now) > 0

    if not valid_token:
        session.Session.connect(stay_connected=False)
        paraloq_file.cached_bearer["bearer"] = session.Session._BEARER_
        paraloq_file.cached_bearer["expires_at"] = str(
            session.Session._SESSION_["expires_at"].timestamp()
        )
        paraloq_file.commit()

        if verbose:
            click.echo("Login successful")

    elif verbose:
        click.echo("You are already logged in")


def _logout(verbose: bool = True):

    paraloq_file = ParaloqConfig.from_disc()
    paraloq_file.cached_bearer = {}
    paraloq_file.commit()
    if verbose:
        click.echo("Logout successful")


@click.group("paraloq")
def paraloq():
    pass


@paraloq.command()
def login():
    _login(verbose=True)


@paraloq.command()
def erase():
    ParaloqConfig.erase()


@paraloq.command()
def logout():
    _logout(verbose=True)


@paraloq.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.argument("name")
@click.argument("pip_args", nargs=-1, type=click.UNPROCESSED)
def install(name, pip_args=None):
    """Install paraloq modules from the paraloq package repository. PIP_ARGS will be forwarded to
    pip install"""
    pip_args = pip_args or tuple()
    if name not in ["core", "validation", "lgd"]:
        raise NotImplementedError

    # Login if necessary
    _login(verbose=False)
    # Prepare the arguments that will be forwarded to pip install
    if len(pip_args) > 0:
        pip_args = " " + " ".join(pip_args)
    else:
        pip_args = ""

    paraloq_file = ParaloqConfig.from_disc()

    token_response = requests.get(
        url=paraloq_file.api_url + "/v1/codeartifact/get-authentication-token",
        headers={
            "Authorization": "Bearer " + paraloq_file.cached_bearer["bearer"],
            "Content-Type": "application/json",
        },
    )
    token_response = json.loads(token_response.text)
    token = token_response["authorizationToken"]
    hive_account = token_response["hiveAccount"]
    repo_url = (
        f"https://aws:{token}@paraloq-{hive_account}"
        f".d.codeartifact.eu-central-1.amazonaws.com/pypi/paraloq/simple/"
    )

    os.system(f"pip config set global.index-url {repo_url}")
    try:
        command = f"pip install paraloq-{name}{pip_args}"
        click.echo(f"Installing using command: {command}")
        os.system(command)
    finally:
        os.system("pip config unset global.index-url")


@paraloq.command()
@click.argument("template")
def init(template: str = "lgd"):
    """
    Initiate a new a new paraloq project
    Args:
        template: The name of the template to use for the project.
    """
    if template == "lgd":
        try:
            import paraloq.lgd
        except ImportError:
            click.echo(
                "You must first install the paraloq lgd module by running 'pq install lgd'"
            )
            exit(1)
        template_dir = os.path.join(
            re.sub("__init__.py", "", paraloq.lgd.__file__), "_cookiecutter"
        )

    else:
        click.echo(f"No such template: {template}")
        exit(2)

    cookiecutter(template_dir)
