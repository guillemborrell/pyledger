#!/usr/bin/env python

#    Pyledger. A simple ledger for smart contracts implemented in Python
#    Copyright (C) 2017  Guillem Borrell Nogueras
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
      setup_requires=['pytest-runner', 'pytest'],
      install_requires=['protobuf>=3.0.0', 'tornado', 'dill', 'sqlalchemy'],
      entry_points={
          'console_scripts': ['pyledger-server=pyledger.server:main',
                              'pyledger-shell=pyledger.clients:run_repl']
          }
      )
