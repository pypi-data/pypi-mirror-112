from os.path import join, dirname
from setuptools import setup, find_packages

with open(join(dirname(__file__), 'elasticsearch_logger/_version.py')) as f:
    exec(f.read())

setup(
    name='elasticsearch-logger',
    version=version,
    description='Library for logging to Elastic Search.',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    url='https://github.com/mmedek/es-logger',
    author='Michal Medek',
    author_email='mmedek94@gmail.com',
    packages=find_packages(),
    keywords='logging, es, elastic search',
    install_requires=[
        'elasticsearch>=7.10.1'
    ],
    platforms=['any'],
    zip_safe=False
)