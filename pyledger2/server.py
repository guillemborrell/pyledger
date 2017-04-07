from autobahn.asyncio.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
import asyncio


class Protocol(WebSocketServerProtocol):
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
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))


def run_server(protocol, address="ws://127.0.0.1:9000"):
        factory = WebSocketServerFactory(address)
        factory.protocol = protocol
        loop = asyncio.get_event_loop()
        server = loop.create_server(factory,
                                    '0.0.0.0',
                                    int(address.split(':')[2])
                                    )
        task = loop.run_until_complete(server)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            task.close()
            loop.close()


if __name__ == '__main__':
    run_server(Protocol)
