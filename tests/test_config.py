import json
import os
import pathlib

from aet.config import Config


def test_config_inits():
    config = Config()
    assert config.aet_host == config.default_aet_host


def test_config_to_dict():
    config = Config()
    assert 'aet_token' in config.to_dict().keys()


def test_config_to_json(tmpdir):
    config = Config(aet_token='testtoken')
    assert '***' in config.to_json()


def test_config_to_dict(tmpdir):
    config = Config()
    assert str(pathlib.Path.home()) in str(config.to_dict()['aet_home_dir'])

    config = Config(aet_token=None, aet_home_dir=str(tmpdir))
    data = json.loads(config.to_json())
    assert data['aet_token'] == None


def test_config_loads_env_vars():
    os.environ['AET_HOST'] = 'aethost'
    os.environ['AET_TOKEN'] = 'testtoken'

    config = Config()
    assert config.aet_host == 'aethost'
    assert config.aet_token == 'testtoken'


def test_config_saves_credentials(tmpdir):
    config = Config(aet_home_dir=tmpdir)
    credentials = {'data': {'attributes': {'token': 'testtoken'}}}
    config.save_credentials(credentials)

    os.environ['AET_TOKEN'] = ''
    config = Config(aet_home_dir=tmpdir)
    assert config.aet_token == 'testtoken'