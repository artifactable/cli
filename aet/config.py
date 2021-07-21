
import os
import pathlib
import json
import subprocess


class ConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pathlib.Path):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class Config(object):

    default_aet_host = 'https://aet-api-prod.herokuapp.com' 
    default_aet_token = None
    default_aet_home_dir = pathlib.Path.home() / '.aet'
    default_dbt_project_dir = pathlib.Path()
    default_dbt_target_dir = default_dbt_project_dir / 'target'

    secrets = [
        'aet_token'
    ]

    def __init__(self, aet_host=None, aet_token=None, aet_home_dir=None,
                 dbt_project_dir=None, dbt_target_dir=None):
        if aet_home_dir:
            self.aet_home_dir = pathlib.Path(aet_home_dir)
        else:
            self.aet_home_dir = self.default_aet_home_dir
        self.aet_credentials_path = self.aet_home_dir / 'user.json'
        self.dbt_project_dir = dbt_project_dir or self.default_dbt_project_dir
        self.dbt_target_dir = dbt_target_dir or self.default_dbt_target_dir
        self.aet_host = aet_host or os.environ.get('AET_HOST') or self.default_aet_host
        self.aet_token = aet_token or os.environ.get('AET_TOKEN') or self.load_saved_token() or self.default_aet_token
        self.git_branch = self.load_git_branch()

    def to_dict(self):  
        return {
            'aet_host': self.aet_host,
            'aet_token': self.aet_token,
            'aet_home_dir': self.aet_home_dir,
            'aet_credentials_path': self.aet_credentials_path,
            'dbt_project_dir': self.dbt_project_dir,
            'dbt_target_dir': self.dbt_target_dir,
            'git_branch': self.git_branch
        }

    def to_json(self):
        data = self.to_dict()
        for secret in self.secrets:
            if secret in data and data[secret] is not None:
                data[secret] = '***'
        return json.dumps(data, indent=2, cls=ConfigEncoder)

    def load_git_branch(self):
        resp = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True)
        if resp.returncode == 0:
            return resp.stdout.decode().strip()
        else:
            return None
    
    def load_saved_token(self):
        if os.path.exists(self.aet_credentials_path):
            with open(self.aet_credentials_path, 'r') as fh:
                try:
                    credentials = json.load(fh)
                    return credentials['data']['attributes']['token']
                except (json.JSONDecodeError, KeyError) as err:
                    print(f"Invalid credential file at {self.aet_credentials_path}. "
                          f"Please try logging in again.")
                    return None
        else:
            return None


    def save_credentials(self, credentials: dict):
        if not os.path.isdir(self.aet_home_dir):
            os.mkdir(self.aet_home_dir)
        with open(self.aet_credentials_path, 'w') as fh:
            json.dump(credentials, fh, indent=2)

