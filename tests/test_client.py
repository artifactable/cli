from aet.client import Client
from aet.config import Config


def test_client_can_get():
    client = Client(config=Config())
    resp = client.get('/healthcheck')
    assert resp.status_code == 200