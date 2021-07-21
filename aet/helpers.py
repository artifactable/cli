import json
import os


from .config import Config


# This should probably be a method on the Config object
def save_credentials(user):
    config = Config()

    if not os.path.isdir(config.aet_home_dir):
        os.mkdir(config.aet_home_dir)
    with open(config.aet_credentials_path, 'w') as fh:
        json.dump(user, fh, indent=2)


# The token should probably be retrieved by querying the config object
def load_token():
    config = Config()

    if config.aet_token:
        return aet_token
    elif os.path.exists(config.aet_credentials_path):
        with open(config.aet_credentials_path, 'r') as fh:
            credentials = json.load(fh)
            return credentials['data']['attributes']['token']
    else:
        return None
