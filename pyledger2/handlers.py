from .pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from google.protobuf.message import DecodeError
import inspect


class Handler:
    def __init__(self):
        self.methods = []
        self.attributes = None

    def activation(self, message):
        pass

    def authentication(self, message):
        pass

    def api(self, message):
        pass

    def key(self, message):
        pass

    def echo(self, message):
        pass

    def contracts(self, message):
        pass

    def status(self, message):
        pass

    def verify(self, message):
        pass

    def call(self, message):
        pass


def handler_methods(handler):
    member_list = inspect.getmembers(handler, predicate=inspect.ismethod)
    return [pair[0] for pair in member_list]


def handle_request(payload):
    handler = Handler()
    message = PyledgerRequest()
    response = PyledgerResponse()

    try:
        message.ParseFromString(payload)
    except DecodeError:
        response.successful = False
        response.data = 'Message not properly formatted'.encode('utf-8')
        return response

    if message.request not in handler_methods(handler):
        response.successful = False
        response.data = 'Request type not available'.encode('utf-8')
        return response

    if message.request == 'activation':
        response.successful = True
        response.data = 'This is a stub'
        return response


def serialize_for_testing(response):
    return response.SerializeToString()
