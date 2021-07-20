import os
import pathlib

class Config(object):
    aet_host = os.environ.get('AET_HOST', 'https://aet-api-prod.herokuapp.com')
    aet_token = os.environ.get('AET_TOKEN')
    user_home_dir = pathlib.Path.home()
    aet_home_dir = user_home_dir / '.aet'
    aet_credentials_path = aet_home_dir / 'user.json'
    dbt_project_dir = pathlib.Path()
    dbt_target_dir = dbt_project_dir / 'target'
