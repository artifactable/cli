import getpass
import pkg_resources
import click
import os
import json
import yaml
import sys

from .client import Client
from .helpers import (
    load_token, default_project_dir, default_target_dir,
    save_credentials
)


class Context(object):
    pass


@click.group()
@click.pass_context
def cli(ctx):
    token = load_token()
    ctx.obj = Context()
    ctx.obj.token = token


@cli.group()
@click.pass_context
def alerts(ctx):
    """
    Commands for managing alerts
    """

    pass


@alerts.command()
@click.pass_context
def list(ctx):
    client = Client(token=ctx.obj.token)
    resp = client.get('/notifications')
    print(json.dumps(resp.json(), indent=2))


@cli.command()
def version():
    """
    Print version information
    """

    print(pkg_resources.require('aet')[0].version)


@cli.command()
@click.option(
    '--target-dir',
    help="Which directory to look in for the compiled dbt assets "
         "file (run_results.json, manifest.json)",
    default=default_target_dir
)
@click.option(
    '--project-dir',
    default=default_project_dir,
    help="Which directory to look in for the dbt_project.yml file"
)
@click.pass_context
def push(ctx, target_dir, project_dir):
    """
    Send alerts about the latest run or test command
    """

    client = Client(token=ctx.obj.token)
    run_results_file = os.path.join(target_dir, 'run_results.json')
    manifest_file = os.path.join(target_dir, 'manifest.json')
    dbt_project_file = os.path.join(project_dir, 'dbt_project.yml')

    run_results_json = json.loads(open(run_results_file, 'r').read())
    manifest_json = json.loads(open(manifest_file, 'r').read())
    dbt_project_json = yaml.load(open(dbt_project_file, 'r').read(),
                                 Loader=yaml.FullLoader)

    data = {
        'run_results': run_results_json,
        'manifest': manifest_json,
        'dbt_project': dbt_project_json
    }

    resp = client.post('/artifacts', data=data)
    print(json.dumps(resp.json(), indent=2))


@cli.command()
@click.pass_context
def login(ctx):
    """
    Log into the aet service
    """

    client = Client(token=ctx.obj.token)

    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")

    resp = client.post('/login', data={
        'email': email,
        'password': password
    })

    if resp.ok:
        save_credentials(resp.json())
        print("Successfully logged in")
    else:
        print(resp.json())


@cli.command()
@click.pass_context
def register(ctx):
    """
    Register a new account
    """

    client = Client(token=ctx.obj.token)

    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    password2 = getpass.getpass("Confirm password: ")

    if password != password2:
        print("Passwords do match")
        sys.exit(1)

    resp = client.post('/users', data={
        'email': email,
        'password': password
    })

    if resp.ok:
        save_credentials(resp.json())
        print()
        print("Successfully created account")
    else:
        print(resp.json())
