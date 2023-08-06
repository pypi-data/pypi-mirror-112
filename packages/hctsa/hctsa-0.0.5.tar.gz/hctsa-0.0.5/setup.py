#from distutils.core import setup
from setuptools import find_packages, setup

setup(
    name = 'hctsa',
    packages = find_packages(),
    version = '0.0.5',  # Ideally should be same as your GitHub release tag version
    description = 'Human-Centered TimeSeries Analysis Package',
    author = 'Andre Sekulla',
    author_email = 'andreseku@gmail.com',
    url = 'https://github.com/AndreSeku/humancenteredTSA',
    download_url = 'https://github.com/AndreSeku/humancenteredTSA/archive/refs/tags/0.0.5.tar.gz',
    keywords = ['timeseries', 'analysis', 'hcml'],
    classifiers = [],
)