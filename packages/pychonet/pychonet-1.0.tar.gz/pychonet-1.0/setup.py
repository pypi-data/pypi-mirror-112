from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='pychonet',
    version='1.0',
    author='Scott Phillips',
    author_email='jrh@example.com',
    packages=['pychonet'],
    url='http://pypi.python.org/pypi/pychonet/',
    license='LICENSE.txt',
    description='A library for interfacing via the ECHONETlite protocol.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
