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

from pyledger2.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest


def auth_info(kwargs):
    user = ''
    password = ''

    if 'user' in kwargs:
        user = kwargs['user']

    if 'password' in kwargs:
        password = kwargs['password']

    return user, password


def session_info(kwargs):
    session = ''

    if 'session' in kwargs:
        session = kwargs['session']

    return session


def call_request(**kwargs):
    request = PyledgerRequest()

    request.user, request.password = auth_info(kwargs)
    request.session_key = session_info(kwargs)
    request.request = 'call'

    if 'contract' not in kwargs:
        raise ValueError('Contract should be a keyword argument')
    request.contract = kwargs['contract']

    if 'call' not in kwargs:
        raise ValueError('Call should be a keyword argument')
    request.call = kwargs['call']

    if 'data' not in kwargs:
        raise ValueError('Data should be a keyword argument')
    request.data = pickle.dumps(kwargs['data'])

    return request.SerializeToString()


def contracts_request(**kwargs):
    # This is simple, doesn't require authentication.
    request = PyledgerRequest()
    request.request = 'contracts'
    return request.SerializeToString()


def api_request(**kwargs):
    request = PyledgerRequest()
    request.request = 'api'

    if 'contract' not in kwargs:
        raise ValueError('Contract should be a keyword argument')

    if kwargs['contract']:
        request.contract = kwargs['contract']
    else:
        raise ValueError('You should give a contract name')

    return request.SerializeToString()


def handle_response(bin_response, callback=None):
    response = PyledgerResponse()
    response.ParseFromString(bin_response)

    if response.successful:
        if callback:
            response_data = pickle.loads(response.data)
            print('Executing callback...')
            callback(response_data)
            return True, response_data
        else:
            return True, pickle.loads(response.data)

    else:
        return False, response.data.decode('utf-8')
