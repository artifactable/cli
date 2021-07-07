import pkg_resources
import click


@click.group()
def cli():
    pass


@cli.command()
def version():
    """
    Print version information
    """

    print(pkg_resources.require('dbt_admin')[0].version)
