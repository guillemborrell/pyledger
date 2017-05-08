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

from autobahn.asyncio.websocket import WebSocketClientProtocol, \
    WebSocketClientFactory
from asyncio.streams import StreamWriter, FlowControlMixin
from pyledger2.client.repl import parse
from pyledger2.server.pyledger_message_pb2 import PyledgerResponse
import pickle
import os
import sys
import asyncio


reader, writer = None, None


async def stdio(loop=None):
    if loop is None:
        loop = asyncio.get_event_loop()

    reader = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(reader)

    writer_transport, writer_protocol = await loop.connect_write_pipe(FlowControlMixin, os.fdopen(0, 'wb'))
    writer = StreamWriter(writer_transport, writer_protocol, None, loop)

    await loop.connect_read_pipe(lambda: reader_protocol, sys.stdin)

    return reader, writer


async def async_input(message, protocol):
    if isinstance(message, str):
        message = message.encode('utf8')

    global reader, writer
    if (reader, writer) == (None, None):
        reader, writer = await stdio()

    writer.write(message)
    await writer.drain()

    line = await reader.readline()
    # This is where everything happens in the client side
    return parse(line, protocol=protocol)

    
class MyClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        print("Connected to server: {0}".format(response.peer))

    async def onOpen(self):
        print("Pyledger REPL client, write 'help' for help or 'help command' for help "
              "on a specific command")

        while True:
            success, message = await async_input('PL >>> ', self)
            if success:
                self.sendMessage(message)

            if message == 'Successfully closed, you can kill this with Ctrl-C':
                break

            await asyncio.sleep(0.1)

    def onMessage(self, payload, isBinary):
        if isBinary:
            response = PyledgerResponse()
            response.ParseFromString(payload)
            if response.successful:
                print(pickle.loads(response.data))
            else:
                print(response.data)
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(code))


if __name__ == '__main__':
    factory = WebSocketClientFactory('ws://127.0.0.1:9000')
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, '127.0.0.1', 9000)
    loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.shutdown_asyncgens()
        loop.close()
        print('Bye')
