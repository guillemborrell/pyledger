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

import datetime
import pickle

from pyledger2.pyledger_message_pb2 import PyledgerRequest, PyledgerResponse
from pyledger2.server.auth import create_master, create_user
from pyledger2.server.config import LIFETIME
from pyledger2.server.db import User, DB, Permissions, Session
from pyledger2.server.handlers import handle_request

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




