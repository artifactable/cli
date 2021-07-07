from setuptools import setup, find_packages

from cli import __version__

setup(
    name='dbt_admin',    
    version=__version__,
    description='Command line interface for working with dbt-admin.',  
    author='Tom Waterman',
    author_email='tjwaterman99@gmail.com',
    url='https://github.com/dbt-admin/cli', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dbt-admin=cli:main'
        ]
    },
    install_requires=['click']
)