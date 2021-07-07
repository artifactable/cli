from setuptools import setup, find_packages


setup(
    name='aet',    
    version='0.0.1',
    description='Command line interface for working with aet services.',  
    author='Tom Waterman',
    author_email='tjwaterman99@gmail.com',
    url='https://github.com/aet-repos/cli', 
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'aet=aet:main'
        ]
    },
    install_requires=[
        'requests==2.25.1',
        'click==8.0.1'
    ]
)