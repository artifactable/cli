import subprocess

from aet import __version__


def test_version_command():
    resp = subprocess.run(['aet', 'version'], capture_output=True)
    assert resp.stdout.decode().strip() == __version__
