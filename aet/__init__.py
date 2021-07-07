import pkg_resources

from .commands import cli


__version__ = pkg_resources.require('aet')[0].version


def main():
    cli()
