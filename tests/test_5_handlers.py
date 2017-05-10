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

import pickle

from pyledger.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest
from pyledger.server.handlers import handle_request


# Test handlers again now that there are some contracts stored

def test_contracts():
    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'contracts'

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)

    assert response.successful == True

    contracts = pickle.loads(response.data)

    assert set(contracts) == {'MyContract', 'DigitalCurrency'}


def test_api():
    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'api'
    request.contract = 'DigitalCurrency'

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)
    api = pickle.loads(response.data)

    assert response.successful == True
    assert api == {
        'add_account': {'key': str},
        'balance': {'key': str},
        'increment': {'key': str, 'quantity': float},
        'transfer': {'dest': str, 'quantity': float, 'source': str}
    }


def test_status():
    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'status'
    request.contract = 'DigitalCurrency'

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)
    status = pickle.loads(response.data)

    assert response.successful == True
    assert status == {'accounts': {}}
