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

from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from pyledger2.server.handlers import handle_request
from pyledger2.server.contract import register_contract, SimpleContract
from pyledger2.server.db import DB
from pyledger2.server.auth import Permissions, method_allow

import asyncio

loop = asyncio.get_event_loop()


class Protocol(WebSocketServerProtocol):
    contract = None

    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

        # echo back message verbatim
        try:
            response = handle_request(payload)
        except:
            response = b'ERROR'

        self.sendMessage(response, True)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


def run_server(address="ws://127.0.0.1:9000"):
        factory = WebSocketServerFactory(address)
        factory.protocol = Protocol
        server = loop.create_server(factory,
                                    '0.0.0.0',
                                    int(address.split(':')[2])
                                    )
        task = loop.run_until_complete(server)

        try:
            print('Starting event loop...')
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            task.close()
            loop.close()


if __name__ == '__main__':
    DB.sync_tables()

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
    print('Contract registered successfully')

    run_server()
