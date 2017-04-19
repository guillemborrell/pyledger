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
    pass


class SimpleContract(BaseContract):
    """
    Contract that uses SimpleStatus for serialization.

    The goal of this class is to make a contact feel just like a Python class.
    """
    _status_class = SimpleStatus

BaseContract.register(SimpleContract)


def methods(contract):
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


def api(contract):
    api_spec = {}
    contract_methods = methods(contract)
    for method in contract_methods:
        function_spec = {}
        sig = inspect.signature(contract_methods[method])
        for param in sig.parameters:
            function_spec[param] = sig.parameters[param].annotation

        api_spec[method] = function_spec

    return api_spec


def signatures(contract):
    contract_signatures = {}
    contract_methods = methods(contract)
    for k, method in contract_methods.items():
        contract_signatures[k] = inspect.signature(method)

    return contract_signatures


def status(contract):
    all_attributes = inspect.getmembers(
        contract,
        predicate=lambda a: not(inspect.isroutine(a)))

    attributes = {}

    for attribute in all_attributes:
        if not attribute[0].startswith('_'):
            attributes[attribute[0]] = attribute[1]

    print(attributes)

    return contract._status_class(attributes=attributes)


def register_contract(contract, description=''):
    """
    Register a contract and make it
    :param contract:
    :param description:
    :return:
    """
    global contract_registry

    if contract.__class__.__name__ in contract_registry:
        raise ValueError('A contract with the same name already registered')
    else:
        contract_registry[contract.__class__.__name__] = contract

    db_contract = Contract()
    db_contract.name = contract.__class__.__name__
    db_contract.created = datetime.datetime.now()
    db_contract.description = description

    first_status = Status()
    first_status.contract = db_contract
    first_status.when = datetime.datetime.now()
    first_status.attributes = status(contract).dump()
    first_status.key = b'genesis'

    DB.session.add(db_contract)
    DB.session.add(first_status)
    DB.session.commit()
