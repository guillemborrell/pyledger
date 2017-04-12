from pyledger2.db import User, DB, Permissions, Session
from pyledger2.auth import create_master, create_user
from pyledger2.handlers import handle_request
from pyledger2.pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from pyledger2.config import LIFETIME
import datetime
import pickle

DB.sync_tables()


def test_0_master_user():
    """
    Create a master user
    """
    create_master('password')
    user = User.from_name('master')
    assert user.get_permissions() == Permissions.ROOT
    assert user.check_password('password') == True

    # Create dummy session
    session = Session()
    session.user = user
    session.key = 'test_session'
    session.registered = datetime.datetime.now()
    session.until = datetime.datetime.now() + datetime.timedelta(hours=LIFETIME)

    DB.session.add(session)
    DB.session.commit()


def test_1_user():
    """
    Create a normal user
    """
    create_user('user', 'password')
    user = User.from_name('user')
    assert user.get_permissions() == Permissions.USER
    assert user.check_password('password') == True


def test_2_create_user():
    """
    Create a user from the API
    """
    request = PyledgerRequest()
    request.request = 'new_user'
    request.user = 'master'
    request.password = 'password'
    request.session_key = 'test_session'
    request.data = pickle.dumps(('user2', 'new_password'))

    response = PyledgerResponse()
    response.ParseFromString(handle_request(request.SerializeToString()))
    assert response.successful == True
    assert response.data == b'user2'

    user = User.from_name('user2')
    assert user.get_permissions() == Permissions.USER
    assert user.check_password('new_password')


def test_3_create_without_permissions():
    """
    Try to create a user without the permissions
    """
    request = PyledgerRequest()
    request.request = 'new_user'
    request.user = 'user'
    request.password = 'password'
    request.data = pickle.dumps(('user3', 'new_password'))

    response = PyledgerResponse()
    response.ParseFromString(handle_request(request.SerializeToString()))
    assert response.successful == False
    assert response.data == b'Not enough permissions'




