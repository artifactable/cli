import pkg_resources
import click
import os
import json
import yaml

from .client import Client


default_target_dir = 'target'
default_project_dir = '.'


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
