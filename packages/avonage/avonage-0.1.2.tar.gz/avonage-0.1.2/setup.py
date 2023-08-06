#!/usr/bin/env python

from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='avonage',
      version='0.1.2',
      description='Asynchronous Vonage / Nexmo client',
      url='https://github.com/adyachok/avonage',
      author='Andras Gyacsok',
      author_email='atti.dyachok@gmail.com',
      license='MIT',
      packages=['avonage'],
      install_requires=[
          'aiohttp',
      ],
      long_description_content_type='text/markdown',
      long_description=long_description,
      zip_safe=False)
