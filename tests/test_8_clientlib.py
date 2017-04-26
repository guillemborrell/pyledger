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

from pyledger2.client.lib import *
from pyledger2.server.handlers import handle_request


def test_clientlib_call_request():
    request = call_request(call='add_account', user='master',
                           password='password', contract='AuthDigitalCurrency',
                           data={'key': 'another_account'})

    succesful, response = handle_response(handle_request(request))

    assert succesful == True
    assert response == 'another_account'


def test_clientlib_call_request_fail():
    request = call_request(call='add_account', contract='AuthDigitalCurrency',
                           data={'key': 'yet_another_account'})

    successful, response = handle_response(handle_request(request))

    assert successful == False
    assert response == 'Not enough permissions'


def test_clientlib_call_contracts():
    request = contracts_request()
    successful, response = handle_response(handle_request(request))

    assert successful == True
    assert set(response) == {'MyContract', 'DigitalCurrency', 'AuthDigitalCurrency'}


def test_clientlib_call_api():
    request = api_request(contract='AuthDigitalCurrency')
    successful, response = handle_response(handle_request(request))

    assert successful == True
    assert response == {
        'add_account': {'key': str},
        'balance': {'key': str},
        'increment': {'key': str, 'quantity': float},
        'transfer': {'dest': str, 'quantity': float, 'source': str}
    }
