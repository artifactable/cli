import os

from aet.helpers import load_token


def test_load_token():
    os.environ['AET_TOKEN'] = '123'
    assert load_token() == '123'

    del os.environ['AET_TOKEN']
    assert load_token() == None
