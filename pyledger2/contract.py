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

from .db import DB, Contract, Status
from .status import SimpleStatus
import datetime
import inspect
import abc

contract_registry = {}


class BaseContract(abc.ABC):
    @abc.abstractproperty
    def status(self):
        pass


class SimpleContract(BaseContract):
    """
    Contract that uses SimpleStatus for serialization.

    The goal of this class is to make a contact feel just like a Python class.
    """
    status_class = SimpleStatus

    def __init__(self, **kwargs):
        self.keys = (k for k in kwargs)
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def status(self):
        return self.status_class(**{k: getattr(self, k) for k in self.keys})


BaseContract.register(SimpleContract)


def contract_methods(contract):
    """
    Obtain methods from the contract

    :param contract:
    :return:
    """
    methods = {}

    for name, function in inspect.getmembers(contract,
                                             predicate=inspect.ismethod):
        if not name == '__init__':
            methods[name] = function

    return methods


def contract_api(contract):
    api_spec = {}
    methods = contract_methods(contract)
    for method in methods:
        function_spec = {}
        sig = inspect.signature(methods[method])
        for param in sig.parameters:
            function_spec[param] = sig.parameters[param].annotation

        api_spec[method] = function_spec

    return api_spec


def contract_signatures(contract):
    signatures = {}
    methods = contract_methods(contract)
    for k, method in methods.items():
        signatures[k] = inspect.signature(method)

    return signatures


def register_contract(contract, description=''):
    """
    Register a contract and make it
    :param contract:
    :param description:
    :return:
    """
    global contract_registry

    db_contract = Contract()
    db_contract.name = contract.__class__.__name__
    db_contract.created = datetime.datetime.now()
    db_contract.description = description

    contract_registry[contract.__class__.__name__] = contract

    first_status = Status()
    first_status.contract = db_contract
    first_status.when = datetime.datetime.now()
    first_status.attributes = contract.status.dump()
    first_status.key = b'genesis'

    DB.session.add(db_contract)
    DB.session.add(first_status)
    DB.session.commit()