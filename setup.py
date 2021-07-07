from setuptools import setup, find_packages


setup(
    name='dbt_admin',    
    version='0.0.1',
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