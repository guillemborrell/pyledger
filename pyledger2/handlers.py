from .pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from .db import Permissions, User, DB, Session, Contract, Status
from .auth import allow, permissions_registry, create_user
from .config import LIFETIME
from .contract import contract_registry, api, methods
from uuid import uuid4
from google.protobuf.message import DecodeError
from typing import Tuple
import hashlib
import datetime
import inspect
import pickle


class Handler:
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
        """Get the api of the contract"""

        if message.contract not in contract_registry:
            return False, 'User function {} not present'.format(
                message.contract).encode('utf-8')

        return True, pickle.dumps(api(contract_registry[message.contract]))

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
        """
        Returns a serialized list of the available contracts

        :param message: Request from the client
        :return:
        """
        return True, pickle.dumps([k for k in contract_registry])

    def status(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        if message.contract not in contract_registry:
            return False, 'User function {} not present'.format(
                message.contract).encode('utf-8')

        contract_class = contract_registry[message.contract]
        status_instance = contract_class._status_class()
        contract = Contract.from_name(message.contract)
        status = contract.last_status()
        status_instance.load(status.attributes)
        return True, pickle.dumps(status_instance.to_dict())

    def verify(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        pass

    def call(self, message: PyledgerRequest) -> Tuple[bool, bytes]:
        """
        Call handler for contract methods.

        :param message:
        :return:
        """
        if message.contract not in contract_registry:
            return False, 'Contract {} not available'.format(
                message.contract).encode('utf-8')

        contract = contract_registry[message.contract]
        if message.call not in methods(contract):
            return False, 'Method {} not found in contact'.format(
                message.call).encode('utf-8')

        # Get the last status of the contract.
        db_contract = Contract.from_name(message.contract)
        status_data = db_contract.last_status()
        status = contract._status_class()
        status.load(status_data.attributes)

        method = contract.__class__.__dict__[message.call]
        method_args = pickle.loads(message.data)

        # Load additional attributes
        status.user = message.user
        status.session = message.session_key

        # Call the method
        result = method(status, **method_args)

        # Persist the new status
        new_status = Status()
        new_status.contract = db_contract
        new_status.attributes = status.dump()
        new_status.when = datetime.datetime.now()

        # This is the status chain standard
        m = hashlib.sha256()
        m.update(status_data.key)
        m.update(new_status.when.isoformat().encode('utf-8'))
        m.update(new_status.attributes)

        new_status.key = m.digest()
        DB.session.add(new_status)
        DB.session.commit()

        return True, pickle.dumps(result)


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
            result = b'Exception in user function: ' + repr(exc).encode('utf-8')

        response.successful = successful
        response.data = result
        return response.SerializeToString()


def make_server():
    """
    Create a server given a smart contract.
    :param contract:
    :return:
    """
    pass