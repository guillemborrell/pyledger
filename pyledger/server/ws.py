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
from pyledger.server.handlers import handle_request
from pyledger.server.contract import register_contract, SimpleContract
from pyledger.server.db import DB
from pyledger.server.auth import Permissions, method_allow

import asyncio

loop = asyncio.get_event_loop()


class Protocol(WebSocketServerProtocol):
    contract = None
    bcast_topic = 36*b'0'

    def onConnect(self, request):
        self.factory.register(self)
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        try:
            topic = payload[:36]
            payload = payload[36:]
            response = handle_request(payload)
        except:
            response = b'ERROR'

        if topic == 36*b'0':
            self.factory.broadcast(topic + response)
        else:
            self.sendMessage(topic + response, True)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))

    def _connectionLost(self, reason):
        WebSocketServerProtocol._connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """
    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print("broadcasting message '{}' ..".format(msg))
        for c in self.clients:
            c.sendMessage(msg, True)
            print("message sent to {}".format(c.peer))


def run_server(address="ws://127.0.0.1:9000"):
        factory = BroadcastServerFactory(address)
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

    # Base contract for testing

    class DigitalCurrency(SimpleContract):
        accounts = {}

        def add_account(self, key: str):
            if key in self.accounts:
                raise Exception('Account already exists')

            self.accounts[key] = 0.0
            return key

        def increment(self, key: str, quantity: float):
            if key not in self.accounts:
                raise Exception('Account not found')

            self.accounts[key] += quantity

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

        def balance(self, key: str):
            if key not in self.accounts:
                print(self.accounts)
                raise Exception('Account not found')

            return str(self.accounts[key])

    register_contract(DigitalCurrency())
    print('Contract registered successfully')

    run_server()
