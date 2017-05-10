import pickle

from pyledger.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest
from pyledger.server.auth import method_allow, Permissions
from pyledger.server.contract import SimpleContract, register_contract
from pyledger.server.handlers import handle_request


def test_0_register_auth_contract():
    class AuthDigitalCurrency(SimpleContract):
        accounts = {}

        @method_allow(Permissions.ROOT)
        def add_account(self, key: str):
            if key in self.accounts:
                raise Exception('Account already exists')

            self.accounts[key] = 0.0
            return key

        @method_allow(Permissions.ROOT)
        def increment(self, key: str, quantity: float):
            if key not in self.accounts:
                raise Exception('Account not found')

            self.accounts[key] += quantity

        @method_allow(Permissions.USER)
        def transfer(self, source: str, dest: str, quantity: float):
            if source not in self.accounts:
                raise Exception('Source account not found')
            if dest not in self.accounts:
                raise Exception('Destination account not found')
            if self.accounts[source] < quantity:
                raise Exception('Not enough funds in source account')
            if quantity < 0:
                raise Exception('You cannot transfer negative currency')

            self.accounts[source] -= quantity
            self.accounts[dest] += quantity

        @method_allow(Permissions.USER)
        def balance(self, key: str):
            if key not in self.accounts:
                print(self.accounts)
                raise Exception('Account not found')

            return str(self.accounts[key])

    register_contract(AuthDigitalCurrency())

    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'call'
    request.contract = 'AuthDigitalCurrency'
    request.call = 'add_account'
    request.data = pickle.dumps({'key': 'new_account'})

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)

    assert response.successful == False
    assert response.data == b'Not enough permissions'


def test_access_contract_as_root():
    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'call'
    request.contract = 'AuthDigitalCurrency'
    request.call = 'add_account'
    request.user = 'master'
    request.password = 'password'
    request.data = pickle.dumps({'key': 'new_account'})

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)

    assert response.successful == True

    response_data = pickle.loads(response.data)
    assert response_data == 'new_account'
