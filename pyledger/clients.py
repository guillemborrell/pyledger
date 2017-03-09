import cmd
import sys
import json
import argparse
from tornado.httpclient import HTTPClient
from urllib import parse


class REPL(cmd.Cmd):
    parser = argparse.ArgumentParser(description='Pyledger client')
    parser.add_argument('--server',
                        help='Url of the ledger server',
                        type=str,
                        default='http://localhost:8888')

    args = parser.parse_args()

    intro = 'PyLedger simple client'
    server = args.server
    prompt = '({})> '.format(args.server)

    def do_exit(self, arg):
        """
        Exits the client

        :param arg:
        :return:
        """
        sys.exit(0)

    def do_key(self, arg):
        """Request a user key"""
        client = HTTPClient()
        response = client.fetch('{}/new_user'.format(
            self.server
        ))
        print(response.body.decode('utf-8'))

    def do_contracts(self, arg):
        """
        List the available contracts in the ledger

        :param arg:
        :return:
        """
        client = HTTPClient()
        response = client.fetch('{}/contracts'.format(
            self.server
        ))
        contracts = json.loads(response.body.decode('utf-8'))
        for c in contracts:
            print('    ', c)

    def do_api(self, arg):
        """
        Check the contract api to use the call function

        :param arg: The name of the contract
        :return:
        """
        client = HTTPClient()
        response = client.fetch('{}/api?{}'.format(
            self.server,
            parse.urlencode({'contract': '{}'.format(arg)})
        ))
        api = json.loads(response.body.decode('utf-8'))
        if type(api) == str:
            print("Contract not found")
            return

        for function, signature in api.items():
            signature = ', '.join(['{} [{}]'.format(
                var, annotation) for var, annotation in signature.items()])

            print('  ', function, '(', signature, ')')

        print('')

    def do_call(self, arg):
        """
        Call function from the contract

        call contract function argument1 argument2 argument3 ...
        """
        contract, function, *arguments = arg.split()
        client = HTTPClient()
        response = client.fetch('{}/api?{}'.format(
            self.server,
            parse.urlencode({'contract': '{}'.format(contract)})
        ))
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

        response = client.fetch('{}/call?{}'.format(
            self.server,
            parse.urlencode(call_dict)
        ))

        print(response.body.decode('utf-8'))


def run_repl():
    REPL().cmdloop()
