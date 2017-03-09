import pytest
from pyledger.contract import Builder, commit_contract, ls_contracts, get_contract, \
    update_status, get_api
from pyledger.db import DB

# Create the tables for the tests.
DB.sync_tables()


def test_0props():
    contract = Builder()
    def add_account(props, key):
        props.accounts[key] = 0
        return props

    with pytest.raises(ValueError) as excinfo:
        contract.add_method(add_account)

    
def test_1signature():
    contract = Builder()
    def add_account(props, key):
        props.accounts[key] = 0.0
        return props

    with pytest.raises(ValueError) as excinfo:
        contract.add_method(add_account)
    

def test_2builder():
    contract = Builder()
    
    def add_account(props, key: str):
        props.accounts[key] = 0.0
        return props
    
    def increment(props, key: str, quantity: float):
        props.accounts[key] += quantity
        return props
    
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)

    assert [k for k in contract.api()[1].keys()] == ['add_account', 'increment']


def test_3call():
    contract = Builder()
    
    def add_account(props, key: str):
        props.accounts[key] = 0.0
        return props
    
    def increment(props, key: str, quantity: float):
        props.accounts[key] += quantity
        return props
    
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    assert contract.call('add_account', key='My_account') == 'SUCCESS'
    

def test_4commit():
    contract = Builder(name='New contract')
    
    def add_account(props, key: str):
        props.accounts[key] = 0.0
        return props
    
    def increment(props, key: str, quantity: float):
        props.accounts[key] += quantity
        return props
    
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    commit_contract(contract)
    contracts = [n for n in ls_contracts()]
    assert contracts == ['New contract']


def test_5get_contract():
    contract = get_contract('New contract')
    contract.call('add_account', key='My_account')
    contract.call('increment', key='My_account', quantity=100.0)
    update_status(contract)

    contract = get_contract('New contract')
    assert contract.get_property('accounts') == {'accounts': {'My_account': 100.0}}


def test_6get_wrong_contract():
    with pytest.raises(ValueError) as excinfo:
        contract = get_contract('Another contract')


def test_7get_api():
    api = get_api('New contract')
    assert api == {'add_account': {'key': 'str'},
                   'increment': {'key': 'str', 'quantity': 'float'}
    }
        
        
if __name__ == '__main__':
    test_4commit()
    test_5get_contract()
    
