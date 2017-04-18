from .pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from .db import Permissions, User, DB, Session, Contract, Status
from google.protobuf.message import DecodeError
from typing import Tuple
from .auth import allow, permissions_registry, create_user
from uuid import uuid4
from .config import LIFETIME
import datetime
import inspect
import pickle
import dill


class Handler:
    def __init__(self):
        methods = None

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
        password = message.data.decode('utf-8')
        user = User.from_name(message.user)
        user.set_password(password)
        DB.session.commit()

        return True, message.user.encode('utf-8')

    def api(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def session(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        """
        Get authentication key

        :param message:
        :return:
        """
        user = User.from_name(message.user)
        session = Session()
        session.user = user
        session.key = str(uuid4())
        session.registered = datetime.datetime.now()
        session.until = datetime.datetime.now() + datetime.timedelta(hours=LIFETIME)

        DB.session.add(session)
        DB.session.commit()

        return True, session.key.encode('utf-8')

    def echo(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        """
        An echo handler for testing authentication and authorization.

        :param message: Request from the client
        :return:
        """
        return True, b'echo'

    def contracts(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def status(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def verify(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def call(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass


def handler_methods(handler):
    """
    Obtain the methods of the handler. Utility funciton in case some
    method is added sometime in the future.

    :param handler:
    :return:
    """
    member_list = inspect.getmembers(handler, predicate=inspect.ismethod)
    return [pair[0] for pair in member_list]


def handle_request(payload: bytes):
    """
    Handle a single request

    :param payload: Serialized PyledgerRequest message
    :return:
    """
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
                response.data = b'Wrong user and/or password'
                return response.SerializeToString()

            if user.get_permissions().value > permission_required.value:
                response.successful = False
                response.data = b'Not enough permissions'
                return response.SerializeToString()

            session = Session.from_key(message.session_key)

            if not session:
                response.successful = False
                response.data = b'Session not available'
                return response.SerializeToString()

            if not session.user == user:
                response.successful = False
                response.data = b'Session not owned by this user'
                return response.SerializeToString()

            if session.until < datetime.datetime.now():
                response.successful = False
                response.data = b'Session expired, restart your client'
                return response.SerializeToString()

        # Select the function from the handler
        try:
            successful, result = getattr(handler, message.request)(message)
        except Exception as exc:
            successful = False
            result = 'Exception in user function: {}'.format(exc).encode('utf-8')

        response.successful = successful
        response.data = result
        return response.SerializeToString()


def contract_methods(contract):
    """
    Obtain methods from the contract

    :param contract:
    :return:
    """
    methods = []
    for name, function in inspect.getmembers(contract,
                                             predicate=inspect.isfunction):
        methods.append(function)

    return methods


def register_contract(contract, **kwargs):
    """
    Register a contract and make it
    :param contract:
    :return:
    """
    contract = Contract()
    contract.name = contract.__name__
    contract.created = datetime.datetime.now()

    if 'description' in kwargs:
        contract.description = kwargs['description']

    contract.methods = dill.dumps(contract_methods(contract))


def make_server():
    """
    Create a server given a smart contract.
    :param contract:
    :return:
    """
    pass