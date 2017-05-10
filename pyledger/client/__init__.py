from pyledger.client.ws import WebSocketClientFactory
from pyledger.client.ws import MyClientProtocol
import asyncio
import argparse


parser = argparse.ArgumentParser(description='Run the pyledger client')
parser.add_argument('--address',
                    help="Address to connect to. Defaults to 127.0.0.1",
                    default='127.0.0.1')
parser.add_argument('--port',
                    help="Port to connect to. Defaults to 9000",
                    default='9000')


def run():
    args = parser.parse_args()
    factory = WebSocketClientFactory('ws://{}:{}'.format(args.address,
                                                         args.port))
    factory.protocol = MyClientProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_connection(factory, args.address, int(args.port))
    loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.shutdown_asyncgens()
        loop.close()
        print('Bye')
