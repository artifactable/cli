import pkg_resources
import click
import os
import json

from .client import Client


class Context(object):
    pass


@click.group()
@click.pass_context
def cli(ctx):
    token = os.environ.get('AET_ADMIN_TOKEN')
    ctx.obj = Context()
    ctx.obj.token = token


@cli.command()
def version():
    """
    Print version information
    """

    print(pkg_resources.require('aet')[0].version)


@cli.command()
@click.pass_context
def push(ctx):
    """
    Upload dbt artifacts to aet
    """

    client = Client(token=ctx.obj.token)

    with open('./target/run_results.json', 'r') as f:
        artifact = json.load(f)
    resp = client.post('/artifacts', data={'artifact': artifact})
    print(resp)
