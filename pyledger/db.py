from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from pyledger.config import args


class Handler():
    def __init__(self):
        self.engine = create_engine(args.db, echo=args.debug)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.Model = declarative_base(bind=self.engine)

    def sync_tables(self):
        self.Model.metadata.create_all(self.engine)


DB = Handler()
Model = DB.Model

# Now the models


class Contract(Model):
    __tablename__ = 'contracts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    created = Column(DateTime)
    methods = Column(LargeBinary)
    api = Column(LargeBinary)
    signatures = Column(LargeBinary)
    status = relationship("Status", back_populates="contract")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="contracts")


class Status(Model):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'))
    contract = relationship("Contract", back_populates="status")
    attributes = Column(LargeBinary)
    key = Column(LargeBinary)
    when = Column(DateTime)
    owner = Column(String)

    def __repr__(self):
        return '<Status key: {}>'.format(self.key)


class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    when = Column(DateTime)
    info = Column(LargeBinary)
    key = Column(String)
    contracts = relationship("Contract", back_populates="user")

    def __repr__(self):
        return '<User key: {}>'.format(self.key)
