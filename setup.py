#!/usr/bin/env python

from setuptools import setup

__version__ = None
with open('pyledger/__init__.py') as f:
    exec(f.read())


setup(name='pyledger',
      version=__version__,
      description='A simple ledger useful to understand DLT (blockchain)',
      author='Guillem Borrell',
      author_email='guillemborrell@gmail.com',
      packages=['pyledger'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'License :: OSI Approved :: GNU Affero General Public License v3'
      ],
      setup_requires=['pytest-runner'],
      install_requires=['protobuf>=3.0.0', 'requests', 'tornado']
      )
