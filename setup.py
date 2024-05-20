from setuptools import setup, find_packages
from os.path import join, dirname


def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.readlines()


setup(
    name='parser_markets',
    version='1.0.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    author='0gl04q',
)
