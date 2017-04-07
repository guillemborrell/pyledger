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

from sqlalchemy import desc
from uuid import uuid4
from pyledger.db import DB, Contract, Status
from datetime import datetime
import hashlib
import inspect
import base64

try:
    import dill
except ImportError:
    print('Check that you are building the documentation')
    dill = None


class Attrs:
    def __init__(self, **kwargs):
        self.__dict__['store'] = kwargs.copy()
        self.__dict__['attr_keys'] = [k for k in kwargs]
        self.__dict__['_user'] = None

    def __getattr__(self, name):
        if name in self.attr_keys:
            return self.__dict__['store'][name]

        elif name == '_user':
            return self.__dict__['_user']

        elif name == 'attr_keys':
            return self.__dict__['attr_keys']

        else:
            raise AttributeError('Attribute {} not found within {}'.format(
                name, ','.join(self.attr_keys)))

    def __setattr__(self, name, value):
        if name in self.attr_keys:
            self.__dict__['store'][name] = value

        elif name == '_user':
            self.__dict__['_user'] = value

        else:
            raise AttributeError('You cannot set new attributes')

    @property
    def user(self):
        if self._user:
            return self._user
        else:
            raise Exception('Not authenticated')

    def get_attributes(self):
        return self.__dict__['store']

    def __repr__(self):
        return 'Attrs: ' + str(self.attr_keys)


class Builder:
    def __init__(self, name='', obj=None):
        if obj is None:
            self.attributes = {}
            self.methods = {}
        else:
            raise NotImplemented('Inspecting from class not supported yet')

        if name:
            if ' ' in name:
                raise ValueError(
                    'The name of the contract should include no spaces')
            self.name = name
        else:
            self.name = str(uuid4())

        self.description = ''

    def add_description(self, description: str):
        self.description = description

    def add_attribute(self, name: str, value):
        """
        Add attribute *name* to the contract with an initial value of *value*
        """
        self.attributes[name] = value

    def add_method(self, method, name: str = ''):
        """
        Add a method to the contract
        """
        if not name:
            name = method.__name__

        sig = inspect.signature(method)

        if 'attrs' not in sig.parameters:
            raise ValueError(
                'The first argument of the method must be'
                ' called attrs and not annotated'
            )
        else:
            for param in sig.parameters:
                if not param == 'attrs' and \
                                sig.parameters[param].annotation == \
                                inspect._empty:
                    raise ValueError(
                        'Parameter {} without signature'.format(
                            param))

        self.methods[name] = method
