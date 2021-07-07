import os
import requests


host = os.environ.get('DBT_ADMIN_HOST',
                      'https://vast-plains-60861.herokuapp.com/api')


class Client(object):

    def __init__(self, token, host=host):
        self.token = token
        self.host = host
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def send(self, method, path, data=None, params={}):
        url = self.host + path
        return requests.request(method, url, headers=self.headers, data=data,
                                params=params)

    def get(self, path, **kwargs):
        return self.send('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.send('POST', path, **kwargs)
