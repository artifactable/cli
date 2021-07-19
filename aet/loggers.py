import click
import json


def log_response(response, message=None, verbose=False):
    if response.ok:
        if verbose:
            status = json.dumps(response.json(), indent=2)
            click.echo(status)
        else:
            message = message or str(response)
            click.echo(message)
    else:
        try:
            click.secho("Error", fg="red")
            errors = response.json()['errors']
            print(json.dumps(errors, indent=2))
        except json.JSONDecodeError:
            click.echo("Response has an error code but "
                       "contains invalid JSON. Please try again.")
        except KeyError:
            click.echo("Response has an error code but no associated errors."
                       " Please try again.")
