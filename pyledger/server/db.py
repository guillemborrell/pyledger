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

import base64
from enum import Enum

from cryptography.exceptions import InvalidKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, \
    LargeBinary
from sqlalchemy import create_engine, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session

from pyledger.server.config import args
from pyledger.server.config import password_backend, SECRET


class Handler:
    def __init__(self):
        self.engine = create_engine(args.db, echo=args.debug)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.Model = declarative_base(bind=self.engine)

    def sync_tables(self):
        self.Model.metadata.create_all(self.engine)


DB = Handler()
Model = DB.Model


# Now the models
class Permissions(Enum):
    ROOT = 1
    USER = 2
    ANON = 3


class Status(Model):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="status")
    attributes = Column(LargeBinary)
    key = Column(LargeBinary, unique=True)  # Crash if there is a key collision.
    when = Column(DateTime)
    owner = Column(String)

    def __repr__(self):
        return '<Status key: {}>'.format(self.key)

    @classmethod
    def query(cls):
        return DB.session.query(cls)


class Contract(Model):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)
    created = Column(DateTime)
    status = relationship("Status", lazy="subquery")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="contracts")

    @classmethod
    def query(cls):
        return DB.session.query(cls)

    @staticmethod
    def from_name(name):
        return Contract.query().filter(Contract.name == name).one_or_none()

    def last_status(self):
        return Status.query().filter(
            Status.contract == self
        ).order_by(desc(Status.when)).first()

    def last_statuses(self):
        return Status.query().filter(
            Status.contract == self
        ).order_by(desc.Status.when).limit(2).all()


class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    when = Column(DateTime)
    info = Column(LargeBinary)
    key = Column(String)
    password = Column(String)
    profile = Column(Integer)
    contracts = relationship("Contract", back_populates="user")
    sessions = relationship("Session", back_populates='user')

    def __repr__(self):
        return '<User {} with key: {}>'.format(self.name, self.key)

    def __str__(self):
        return '<User {} with key: {}>'.format(self.name, self.key)

    def set_password(self, password):
        self.password = base64.b64encode(password)

    def get_password(self):
        return base64.b64decode(self.password)

    def check_password(self, password):
        kpdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=SECRET,
            iterations=1000000,
            backend=password_backend
        )
        try:
            kpdf.verify(password.encode('utf-8'), self.get_password())
            correct = True
        except InvalidKey as e:
            print(e)
            correct = False

        return correct

    @classmethod
    def query(cls):
        return DB.session.query(cls)

    @staticmethod
    def from_name(name):
        return User.query().filter(User.name == name).one_or_none()

    def get_permissions(self):
        return Permissions(self.profile)

    def set_permissions(self, permissions):
        self.profile = permissions.value


class Session(Model):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True)
    registered = Column(DateTime)
    until = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="sessions")

    def __repr__(self):
        return 'Session {}'.format(self.key)

    @classmethod
    def query(cls):
        return DB.session.query(cls)

    @staticmethod
    def from_key(key):
        return Session.query().filter(Session.key == key).one_or_none()


class Task(Model):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    method = Column(String)
    when = Column(DateTime)

    def __repr__(self):
        return 'Task. Scheduled: {}'.format(self.when.isoformat())
