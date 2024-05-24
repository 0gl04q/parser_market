from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.readlines()


setup(
    name='parser_markets',
    version='1.2.1',
    packages=find_packages(),
    install_requires=read_requirements(),
    author='0gl04q',
)
