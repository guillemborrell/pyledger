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

from pyledger2.handlers import Handler, handler_methods, handle_request
from pyledger2.pyledger_message_pb2 import PyledgerResponse, PyledgerRequest


def test_handler_methods():
    assert set(handler_methods(Handler())) == {
        '__init__', 'activation', 'authentication', 'api', 'key', 'echo',
        'contracts', 'verify', 'call', 'status'
    }


def test_failed_message():
    response = PyledgerResponse()
    response.ParseFromString(handle_request(b'xxxyyy'))
    assert response.successful == False
    assert response.data == b'Message not properly formatted'


def test_wrong_request():
    request = PyledgerRequest()
    response = PyledgerResponse()
    request.request = 'blahblah'
    response.ParseFromString(
        handle_request(
            request.SerializeToString()
        )
    )

    assert response.successful == False
    assert response.data == b'Request type not available'
