from .pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from .db import Permissions, User
from google.protobuf.message import DecodeError
from typing import Tuple
from .auth import allow, permissions_registry, create_user
from uuid import uuid4
import inspect
import pickle


class Handler:
    def __init__(self):
        self.methods = []
        self.attributes = None
        self.permissions = {}

    @allow(Permissions.ROOT)
    def new_user(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        """
        Request an activation key

        :param message:
        :return:
        """
        name, password = pickle.loads(message.data)
        create_user(name, password)

        return True, name.encode('utf-8')

    @allow(Permissions.USER)
    def set_password(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def authentication(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def api(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def session(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        """
        Get authentication key

        :param message:
        :return:
        """
        return True, b'0'

    def echo(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        """
        An echo handler for testing authentication and authorization.

        :param message: Request from the client
        :return:
        """

        permissions = check_permissions(message.session_key)

    def contracts(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def status(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def verify(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def call(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
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
        response.data = b'Message not properly formatted'
        return response.SerializeToString()

    if message.request not in handler_methods(handler):
        response.successful = False
        response.data = b'Request type not available'
        return response.SerializeToString()

    else:
        # Handle authentication
        if message.request in permissions_registry:
            user = User.from_name(message.user)
            permission_required = permissions_registry[message.request]

            if not user.check_password(message.password):
                response.successful = False
                response.data = b'Wrong user and or password'
                return response.SerializeToString()

            if user.get_permissions().value > permission_required.value:
                response.successful = False
                response.data = b'Not enough permissions'
                return response.SerializeToString()

        # Select the function from the handler
        print('Calling', message.request)
        try:
            successful, result = getattr(handler, message.request)(message)
        except Exception as exc:
            successful = False
            result = 'Exception in user function: {}'.format(exc).encode('utf-8')

        response.successful = successful
        response.data = result
        return response.SerializeToString()

