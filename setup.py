from setuptools import setup, find_packages


setup(
    name='aet',    
    version='0.0.1',
    description='Command line interface for working with dbt-admin.',  
    author='Tom Waterman',
    author_email='tjwaterman99@gmail.com',
    url='https://github.com/aet-repos/cli', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aetn=aet:main'
        ]
    },
    install_requires=['click']
)