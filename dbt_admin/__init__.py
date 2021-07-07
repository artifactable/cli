import pkg_resources

from .commands import cli


__version__ = pkg_resources.require('dbt_admin')[0].version


def main():
    cli()
