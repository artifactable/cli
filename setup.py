from setuptools import setup, find_packages

import aet


setup(
    name='aet',    
    version=aet.__version__,
    description='Command line interface for working with aet services.',  
    author='Tom Waterman',
    author_email='tjwaterman99@gmail.com',
    url='https://github.com/aet-repos/cli', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aet=aet.__main__:cli'
        ]
    },
    install_requires=[
        'requests<2.24.0',
        'click==8.0.1',
        'PyYAML==5.4.1'
    ]
)