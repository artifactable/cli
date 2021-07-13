import json
import os


profile_dir = os.path.join(os.path.expanduser('~'), '.aet')
credentials_path = os.path.join(profile_dir, 'user.json')
default_target_dir = 'target'
default_project_dir = '.'


def save_credentials(user):
    if not os.path.isdir(profile_dir):
        os.mkdir(profile_dir)
    with open(credentials_path, 'w') as fh:
        json.dump(user, fh, indent=2)


def load_token():
    if 'AET_TOKEN' in os.environ:
        return os.environ['AET_TOKEN']
    elif os.path.exists(credentials_path):
        with open(credentials_path, 'r') as fh:
            credentials = json.load(fh)
            return credentials['data']['attributes']['token']
    else:
        return None
