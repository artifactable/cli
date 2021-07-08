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
    token = os.environ.get('AET_TOKEN')
    ctx.obj = Context()
    ctx.obj.token = token


@cli.command()
def version():
    """
    Print version information
    """

    print(pkg_resources.require('aet')[0].version)


@cli.command()
@click.option(
    '--target-path',
    help="Path to dbt target directory",
    default="target"
)
@click.pass_context
def push(ctx, target_path):
    """
    Upload dbt artifacts
    """

    client = Client(token=ctx.obj.token)

    artifact_names = [
        'run_results.json',
        'manifest.json',
        'catalog.json',
    ]

    artifact_paths = [
        os.path.abspath(os.path.join(os.getcwd(), target_path, artifact_name))
        for artifact_name in artifact_names
    ]

    for path in artifact_paths:
        if not os.path.exists(path):
            print(f"Skipping artifact {path.split(os.path.sep)[-1]}."
                  f" No artifact found at {path}")
            continue

        with open(path, 'r') as f:
            try:
                artifact = json.load(f)
            except json.decoder.JSONDecoderError:
                print(f"Invalid artifact: {path}")

            resp = client.post('/artifacts', data={'artifact': artifact})
            if not resp.ok:
                print(f"Failed to load artifact "
                      f"(status={resp.status_code}) {path}")
            else:
                print(f"Loaded artifact {path}")
