from pyledger.contract import ls_contracts, get_api, get_contract, update_status
from pyledger.config import args
from pyledger.db import DB, User
from collections import namedtuple
from datetime import datetime
from uuid import uuid4
import tornado.web
import argparse
import sys
import json


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

        
class NewUserHandler(tornado.web.RequestHandler):
    def get(self):
        new_user = User()
        new_user.key = str(uuid4())
        new_user.info = b''
        new_user.when = datetime.now()
        DB.session.add(new_user)
        DB.session.commit()

        self.write(new_user.key)        

class ContractsHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps([c for c in ls_contracts()]))


class APIHandler(tornado.web.RequestHandler):
    def get(self):
        contract = self.get_argument('contract', default=None)
        if contract is None:
            self.write('You must specify a contract')

        else:
            self.write(get_api(contract))


class CallHandler(tornado.web.RequestHandler):
    def get(self):
        arguments = self.request.arguments
    
        if 'contract' not in arguments:
            self.write('Contract not set')
            return
        else:
            name = arguments.get('contract')[0].decode('utf-8')
            del arguments['contract']
            
        if 'function' not in arguments:
            self.write('function not set')
            return
        else:
            function = arguments.get('function')[0].decode('utf-8')
            del arguments['function']

        api = get_api(name)[function]
            
        for arg in arguments.keys():
            if arg in api:
                if api[arg] == 'int':
                    arguments[arg] = int(arguments[arg][0].decode('utf-8'))
                elif api[arg] == 'float':
                    arguments[arg] = float(arguments[arg][0].decode('utf-8'))
                elif api[arg] == 'str':
                    arguments[arg] = arguments[arg][0].decode('utf-8')

        contract = get_contract(name)

        try:
            response = contract.call(function, **arguments)
        except Exception as e:
            response = str(e)
            
        self.write(response)

        
def make_application():
    return tornado.web.Application(
        [
            (r"/contracts", ContractsHandler),
            (r"/api", APIHandler),
            (r"/call", CallHandler),
            (r"/new_user", NewUserHandler),
            (r"/", MainHandler),
        ],
        db=args.db,
        debug=args.debug)
