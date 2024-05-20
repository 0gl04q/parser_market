from setuptools import setup, find_packages


def read_requirements():
    with open('requirements.txt') as req_file:
        return req_file.readlines()


setup(
    name='parser_markets',
    version='1.0.0',
    packages=find_packages(),
    install_requires=read_requirements(),
    description='Парсер различный площадок',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='0gl04q',
    author_email='rdc_atm@mail.ru',
    url='https://github.com/0gl04q/parser_market',
    classifiers=[
        'Programming Language :: Python :: 3'
    ],
    python_requires='>=3.6'
)
