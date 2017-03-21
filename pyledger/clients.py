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

import cmd
import sys
import json
import argparse
import pprint
from tornado.httpclient import HTTPClient
from urllib import parse


class REPL(cmd.Cmd):
    parser = argparse.ArgumentParser(description='Pyledger client')
    parser.add_argument('--server',
                        help='Url of the ledger server',
                        type=str,
                        default='http://localhost:8888')
    parser.add_argument('--user',
                        help='User key',
                        type=str,
                        default='')

    args = parser.parse_args()

    user_key = ''
    if args.user:
        user_key = args.user

    intro = 'PyLedger simple client'
    server = args.server
    prompt = '({})> '.format(args.server)
    client = HTTPClient()

    def request(self, url, **args):
        return self.client.fetch('{}{}?{}'.format(self.server,
                                                  url,
                                                  parse.urlencode(args)),
                                 headers={'X-User': self.user_key})

    def do_exit(self, arg):
        """
        Exits the client

        :param arg:
        :return:
        """
        self.client.close()
        sys.exit(0)

    def do_key(self, arg):
        """
        Request a user key::

            ()> key name_of_user

        Prints the key of the new user.
        """
        response = self.request('/new_user', name=arg)
        print(response.body.decode('utf-8'))

    def do_contracts(self, arg):
        """
        List the available contracts in the ledger

        :param arg:
        :return:
        """
        response = self.request('/contracts')
        contracts = json.loads(response.body.decode('utf-8'))
        for c in contracts:
            print('    ', c)

    def do_api(self, arg):
        """
        Check the contract api to use the call function

        :param arg: The name of the contract
        :return:
        """

        response = self.request('/api', contract=arg)

        api = json.loads(response.body.decode('utf-8'))
        if type(api) == str:
            print("Contract not found")
            return

        for function, signature in api.items():
            signature = ', '.join(['{} [{}]'.format(
                var, annotation) for var, annotation in signature.items()])

            print('  ', function, '(', signature, ')')

        print('')

    def do_status(self, arg):
        """
        Check the contract current status of the attributes

        Usage.

        Get the last status of the contract and check its consistency::

            ()> status ContractName

        Dump all the statuses of the contract to a given file::

            ()> status ContractName dump /file/path

        """
        if ' ' not in arg:
            query_args = {'contract': '{}'.format(arg)}
            dump = False

        elif len(arg.split()) == 3:
            args = arg.split()
            query_args = {'contract': '{}'.format(args[0]),
                          'data': True}
            dump = True
        else:
            print('Command could not be parsed')
            return

        response = self.client.fetch('{}/status?{}'.format(
            self.server,
            parse.urlencode(query_args)
        ))

        if dump:
            print('Contract data dump at', args[2])
            with open(args[2], 'wb') as f:
                f.write(response.body)
        else:
            status = json.loads(response.body.decode('utf-8'))
            pprint.pprint(status)

    def do_verify(self, arg):
        """
        Verify the consistency of all the statuses of the contract

        :param arg: The name of the contract
        :return:
        """
        response = self.client.fetch('{}/verify?{}'.format(
            self.server,
            parse.urlencode({'contract': '{}'.format(arg)})
        ))
        status = json.loads(response.body.decode('utf-8'))
        pprint.pprint(status)

    def do_call(self, arg):
        """
        Call function from the contract

        call contract function argument1 argument2 argument3 ...
        """
        contract, function, *arguments = arg.split()
        response = self.request('/api', contract=contract)
        api = json.loads(response.body.decode('utf-8'))

        if type(api) == str:
            print("Contract not found")
            return

        if function not in api:
            print("Function not found")
            return

        signature = [v for v in api[function]]

        call_args = {sig: val for sig, val in zip(signature, arguments)}
        call_dict = {'contract': contract,
                     'function': function}
        call_dict.update(call_args)
        response = self.request('/call', **call_dict)

        print(response.body.decode('utf-8'))


def run_repl():
    REPL().cmdloop()


