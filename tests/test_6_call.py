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

from pyledger2.handlers import handle_request
from pyledger2.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest
import pickle


def test_simple_call():
    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'call'
    request.contract = 'DigitalCurrency'
    request.call = 'add_account'
    request.data = pickle.dumps({'key': 'new_account'})

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)

    response_data = pickle.loads(response.data)

    assert response.successful == True
    assert response_data == response_data


def test_exception():
    request = PyledgerRequest()
    response = PyledgerResponse()

    request.request = 'call'
    request.contract = 'DigitalCurrency'
    request.call = 'increment'
    request.data = pickle.dumps({'key': 'another_account', 'quantity': 100.0})

    byte_request = request.SerializeToString()
    byte_response = handle_request(byte_request)
    response.ParseFromString(byte_response)

    assert response.successful == False
    assert response.data == b"Exception in user function: Exception('Account not found',)"
