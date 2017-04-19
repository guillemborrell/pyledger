from pyledger2.contract import SimpleContract
from pyledger2.status import BaseStatus
from pyledger2.handlers import register_contract


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
    contract.add_account('key1')
    contract.increment('key1', 100.0)
    assert contract.balance('key1')[1] == '100.0'


def test_register_contract():
    class MyContract(SimpleContract):
        def greet(self, name: str):
            self.counter += 1
            return "hello, " + name

    dill
    this_contract = MyContract(counter=0)
    register_contract(this_contract)

    assert False
