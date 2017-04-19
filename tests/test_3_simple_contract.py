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

from pyledger2.contract import SimpleContract, register_contract, \
    contract_methods, contract_api, contract_signatures
from pyledger2.status import BaseStatus
from inspect import Signature, Parameter


def test_new_contract():
    contract = SimpleContract(counter=0)
    contract.counter = 1

    assert contract.counter == 1


def test_contract_status():
    """Check if returns a status"""
    class MyContract(SimpleContract):
        def greet(self, name: str):
            self.counter += 1
            return "hello, " + name

    this_contract = MyContract(counter=0)
    this_contract_status = this_contract.status

    assert isinstance(this_contract_status, BaseStatus) == True


def test_full_contract():
    """Check that a contract feels like a class"""
    class DigitalCurrency(SimpleContract):
        def add_account(self, key: str):
            if key in self.accounts:
                raise Exception('Account already exists')

            self.accounts[key] = 0.0
            return self

        def increment(self, key: str, quantity: float):
            if key not in self.accounts:
                raise Exception('Account not found')

            self.accounts[key] += quantity
            return self

        def transfer(self, source: str, dest: str, quantity: float):
            if source not in self.accounts:
                raise Exception('Source account not found')
            if dest not in self.accounts:
                raise Exception('Destination account not found')
            if self.accounts[source] < quantity:
                raise Exception('Not enough funds in source account')

            self.accounts[source] -= quantity
            self.accounts[dest] += quantity

            return self

        def balance(self, key: str):
            if key not in self.accounts:
                print(self.accounts)
                raise Exception('Account not found')

            return self, str(self.accounts[key])

    contract = DigitalCurrency(accounts={})

    assert [k for k in contract_methods(contract)] == [
        'add_account', 'balance', 'increment', 'transfer']

    assert contract_api(contract) == {
        'add_account': {'key': str},
        'balance': {'key': str},
        'increment': {'key': str, 'quantity': float},
        'transfer': {'dest': str, 'quantity': float, 'source': str}
    }

    assert contract_signatures(contract) == {
        'add_account': Signature(parameters=[
            Parameter('key', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)]),
        'balance': Signature(parameters=[
            Parameter('key', Parameter.POSITIONAL_OR_KEYWORD, annotation=str)]),
        'increment': Signature(parameters=[
            Parameter('key', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('quantity', Parameter.POSITIONAL_OR_KEYWORD, annotation=float)
        ]),
        'transfer': Signature(parameters=[
            Parameter('source', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('dest', Parameter.POSITIONAL_OR_KEYWORD, annotation=str),
            Parameter('quantity', Parameter.POSITIONAL_OR_KEYWORD, annotation=float)
        ])
    }

    contract.add_account('key1')
    contract.increment('key1', 100.0)
    assert contract.balance('key1')[1] == '100.0'


def test_register_contract():
    class MyContract(SimpleContract):
        def greet(self, name: str):
            self.counter += 1
            return "hello, " + name

    this_contract = MyContract(counter=0)
    register_contract(this_contract)

    assert True
