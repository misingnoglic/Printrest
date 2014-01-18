#!/usr/bin/env python

from setuptools import setup

setup(
    name='pinterest-api',
    version='0.0.1',
    description='Pinterest API client',
    author='Pinterest, inc.',
    author_email='api@pinterest.com',
    url='http://pinterest.com',
    install_requires=['requests>=0.14'],
    packages=['pinterest'])
