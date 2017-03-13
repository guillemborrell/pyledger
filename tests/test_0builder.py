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

import pytest
from pyledger.contract import Builder, commit_contract, ls_contracts, get_contract, \
    update_status, get_api
from pyledger.db import DB

# Create the tables for the tests.
DB.sync_tables()


def test_0attrs():
    contract = Builder()

    def add_account(attrs, key):
        attrs.accounts[key] = 0
        return attrs

    with pytest.raises(ValueError) as excinfo:
        contract.add_method(add_account)

    
def test_1signature():
    contract = Builder()

    def add_account(attrs, key):
        attrs.accounts[key] = 0.0
        return attrs

    with pytest.raises(ValueError) as excinfo:
        contract.add_method(add_account)
    

def test_2builder():
    contract = Builder()
    
    def add_account(attrs, key: str):
        attrs.accounts[key] = 0.0
        return attrs
    
    def increment(attrs, key: str, quantity: float):
        attrs.accounts[key] += quantity
        return attrs
    
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)

    assert sorted([k for k in contract.api()[1].keys()]) == ['add_account', 'increment']


def test_3call():
    contract = Builder()
    
    def add_account(attrs, key: str):
        attrs.accounts[key] = 0.0
        return attrs
    
    def increment(attrs, key: str, quantity: float):
        attrs.accounts[key] += quantity
        return attrs
    
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    assert contract.call('add_account', key='My_account') == b'SUCCESS'
    

def test_4commit():
    contract = Builder(name='NewContract')
    
    def add_account(attrs, key: str):
        attrs.accounts[key] = 0.0
        return attrs
    
    def increment(attrs, key: str, quantity: float):
        attrs.accounts[key] += quantity
        return attrs
    
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    commit_contract(contract)
    contracts = [n for n in ls_contracts()]
    assert contracts == ['NewContract']


def test_5get_contract():
    contract = get_contract('NewContract')
    contract.call('add_account', key='My_account')
    contract.call('increment', key='My_account', quantity=100.0)
    update_status(contract)

    contract = get_contract('NewContract')
    assert contract.get_property('accounts') == {'accounts': {'My_account': 100.0}}


def test_6get_wrong_contract():
    with pytest.raises(ValueError) as excinfo:
        contract = get_contract('Another contract')


def test_7get_api():
    api = get_api('NewContract')
    assert api == {'add_account': {'key': 'str'},
                   'increment': {'key': 'str', 'quantity': 'float'}
                   }
        
        
if __name__ == '__main__':
    test_4commit()
    test_5get_contract()
