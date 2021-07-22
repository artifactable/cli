import os
import requests
import logging


logger = logging.getLogger()

class Client(object):

    def __init__(self, config):
        self.config = config
        self.token = self.config.aet_token
        self.host = self.config.aet_host
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        logger.debug(f'Initialized client with token={self.token != None} host={self.host}')

    def send(self, method, path, data=None, params={}):
        url = self.host + path
        return requests.request(method, url, headers=self.headers, json=data,
                                params=params)

    def get(self, path, **kwargs):
        return self.send('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self.send('POST', path, **kwargs)
