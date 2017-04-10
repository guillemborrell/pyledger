from .pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from google.protobuf.message import DecodeError
import inspect
from enum import Enum, auto


class Permissions(Enum):
    MASTER = auto()
    USER = auto()
    ANON = auto()


def check_permissions(key):
    pass


class AuthenticationResponse(Enum):
    AUTHENTICATED = auto()
    NOT_AUTHENTICATED = auto()
    SESSION_EXPIRED = auto()
    BANNED_USER = auto()
    INVALID = auto()


class Handler:
    def __init__(self):
        self.methods = []
        self.attributes = None

    def activation(self, message: PyledgerRequest) -> PyledgerResponse:
        """
        Request for activation key

        :param message:
        :return:
        """
        pass

    def authentication(self, message: PyledgerRequest) -> PyledgerResponse:
        pass

    def api(self, message: PyledgerRequest) -> PyledgerResponse:
        pass

    def key(self, message: PyledgerRequest) -> PyledgerResponse:
        pass

    def echo(self, message: PyledgerRequest) -> PyledgerResponse:
        """
        An echo handler for testing authentication and authorization.

        :param message: Request from the client
        :return:
        """

        permissions = check_permissions(message.session_key)

    def contracts(self, message: PyledgerRequest) -> PyledgerResponse:
        pass

    def status(self, message: PyledgerRequest) -> PyledgerResponse:
        pass

    def verify(self, message: PyledgerRequest) -> PyledgerResponse:
        pass

    def call(self, message: PyledgerRequest) -> PyledgerResponse:
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
        return response.SerializeToString()

    if message.request not in handler_methods(handler):
        response.successful = False
        response.data = 'Request type not available'.encode('utf-8')
        return response.SerializeToString()

    else:
        # Select the function from the handler
        successful, response = getattr(handler, message.request)(message)
        response.successful = successful
        response.response = response
        return response.SerializeToString()

