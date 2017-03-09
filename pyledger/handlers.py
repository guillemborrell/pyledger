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

from pyledger.contract import ls_contracts, get_api, get_contract, \
    commit_contract, update_status
from pyledger.config import args
from pyledger.db import DB, User
from datetime import datetime
from uuid import uuid4
import tornado.web
import tornado.wsgi
import json


# Sync tables here if not under testing environment
if args.sync and not args.test:
    DB.sync_tables()
    print("Warning: Syncing database at {}".format(args.db))


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
            api = get_api(contract)
            if api:
                self.write(api)
            else:
                self.write('"Contract not found"')


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
            print('Calling', function, 'With args', arguments)
            response = contract.call(function, **arguments)
            update_status(contract)

        except Exception as e:
            response = str(e)
            
        self.write(response)

        
def make_tornado(ledger_configuration=None):
    """
    Make a tornado application from the ledger configuration

    :param ledger_configuration:
    :return:
    """
    if ledger_configuration and args.sync:
        contract = ledger_configuration()
        commit_contract(contract)

    elif args.sync:
        print("Warning: No ledger configuration passed to the application "
              "builder. If you are debugging or a power user, you can ignore "
              "this message.")

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


def make_wsgi(ledger_configuration=None):
    """
    Make a WSGI application from the ledger configuration

    :param ledger_configuration:
    :return:
    """
    return tornado.wsgi.WSGIAdapter(make_tornado(ledger_configuration))