import getpass
import pkg_resources
import click
import os
import json
import yaml
import sys

from .client import Client
from .config import Config
from .loggers import log_response


class Context(object):
    pass


@click.group()
@click.option(
    '--verbose/--no-verbose',
    default=False,
    help="Print more verbose output"
)
@click.pass_context
def cli(ctx, verbose):
    config = Config()
    client = Client(config=config)
    ctx.obj = Context()
    ctx.obj.client = client
    ctx.obj.config = config
    ctx.obj.verbose = verbose


@cli.command()
@click.pass_context
def debug(ctx):
    """
    Print configuration information
    """

    print(ctx.obj.config.to_json())


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
    resp = ctx.obj.client.get('/notifications')
    log_response(resp, verbose=True)


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
    default=None
)
@click.option(
    '--project-dir',
    default=None,
    help="Which directory to look in for the dbt_project.yml file"
)
@click.pass_context
def push(ctx, target_dir, project_dir):
    """
    Send alerts about the latest run or test command
    """

    config = Config(dbt_project_dir=project_dir, dbt_target_dir=target_dir)
    client = Client(config=config)

    run_results_file = os.path.join(config.dbt_target_dir, 'run_results.json')
    manifest_file = os.path.join(config.dbt_target_dir, 'manifest.json')
    dbt_project_file = os.path.join(config.dbt_project_dir, 'dbt_project.yml')

    run_results_json = json.loads(open(run_results_file, 'r').read())
    manifest_json = json.loads(open(manifest_file, 'r').read())
    dbt_project_json = yaml.load(open(dbt_project_file, 'r').read(),
                                 Loader=yaml.FullLoader)

    data = {
        'run_results': run_results_json,
        'manifest': manifest_json,
        'dbt_project': dbt_project_json,
        'git_branch': config.git_branch
    }

    resp = client.post('/artifacts', data=data)
    log_response(resp, message="Successfully uploaded artifacts.",
                 verbose=ctx.obj.verbose)


@cli.command()
@click.pass_context
def login(ctx):
    """
    Log into the aet service
    """

    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")

    resp = ctx.obj.client.post('/login', data={
        'email': email,
        'password': password
    })
    if resp.ok:
        ctx.obj.config.save_credentials(resp.json())
    log_response(resp, message="Successfully logged in",
                 verbose=ctx.obj.verbose)


@cli.command()
@click.pass_context
def register(ctx):
    """
    Register a new account
    """

    email = input("Enter email: ")
    password = getpass.getpass("Enter password: ")
    password2 = getpass.getpass("Confirm password: ")

    if password != password2:
        print("Passwords do match")
        sys.exit(1)

    resp = ctx.obj.client.post('/users', data={
        'email': email,
        'password': password
    })

    if resp.ok:
        ctx.obj.config.save_credentials(resp.json())
    log_response(resp, message="Successfully created account")
