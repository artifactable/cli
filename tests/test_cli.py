import subprocess

from artifactable import __version__


def test_version_command():
    resp = subprocess.run(['artifactable', 'version'], capture_output=True)
    assert resp.stdout.decode().strip() == __version__
