import subprocess

from dbt_admin import __version__


def test_version_command():
    resp = subprocess.run(['dbt-admin', 'version'], capture_output=True)
    assert resp.stdout.decode().strip() == __version__
