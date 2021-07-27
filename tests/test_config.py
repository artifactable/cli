import json
import os
import pathlib

from artifactable.config import Config


def test_config_inits():
    config = Config()
    assert config.artifactable_host == config.default_artifactable_host


def test_config_to_dict():
    config = Config()
    assert 'artifactable_token' in config.to_dict()
    assert 'git_branch' in config.to_dict()


def test_config_to_json(tmpdir):
    config = Config(artifactable_token='testtoken')
    assert '***' in config.to_json()


def test_config_to_dict(tmpdir):
    config = Config()
    assert str(pathlib.Path.home()) in str(config.to_dict()['artifactable_home_dir'])

    config = Config(artifactable_token=None, artifactable_home_dir=str(tmpdir))
    data = json.loads(config.to_json())
    assert data['artifactable_token'] == None


def test_config_loads_env_vars():
    os.environ['artifactable_HOST'] = 'artifactablehost'
    os.environ['artifactable_TOKEN'] = 'testtoken'

    config = Config()
    assert config.artifactable_host == 'artifactablehost'
    assert config.artifactable_token == 'testtoken'


def test_config_saves_credentials(tmpdir):
    config = Config(artifactable_home_dir=tmpdir)
    credentials = {'data': {'attributes': {'token': 'testtoken'}}}
    config.save_credentials(credentials)

    os.environ['artifactable_TOKEN'] = ''
    config = Config(artifactable_home_dir=tmpdir)
    assert config.artifactable_token == 'testtoken'