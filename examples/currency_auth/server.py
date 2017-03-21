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

from pyledger.handlers import make_tornado
from pyledger.contract import Builder
from pyledger.config import args
import tornado.ioloop
from uuid import uuid4
from collections import defaultdict


def ledger():
    def add_account(attrs, holder: str):
        if attrs.user.name == 'admin':
            key = str(uuid4())
            attrs.accounts[holder][key] = 0.0
            return attrs, key

        else:
            raise Exception('Only admin can create accounts')

    def increment(attrs, holder: str, key: str, quantity: float):
        if attrs.user.name == 'admin':
            if holder not in attrs.accounts:
                raise Exception('Account owner not registered')
            elif key not in attrs.accounts[holder]:
                raise Exception('Account not found')
            else:
                attrs.accounts[holder][key] += quantity
                return attrs

        else:
            raise Exception('Only admin can create currency')

    def transfer(attrs, source: str, dest: str, quantity: float):
        all_accounts = {}

        # Maps accounts with the holder.
        for owner in attrs.accounts:
            for account in attrs.accounts[owner]:
                all_accounts[account] = owner

        if attrs.user.key not in attrs.accounts:
            raise Exception('User holds no accounts')

        if source not in attrs.accounts[attrs.user.key]:
            raise Exception('Source account not found')

        if dest not in all_accounts:
            raise Exception('Destination account not found')

        if attrs.accounts[attrs.user.key][source] < quantity:
            raise Exception('Not enough funds in source account')

        attrs.accounts[attrs.user.key][source] -= quantity
        attrs.accounts[all_accounts[dest]][dest] += quantity

        return attrs

    def list_accounts(attrs):
        if attrs.user.key not in attrs.accounts:
            raise Exception('User holds no accounts')

        return attrs, '\n'.join(attrs.accounts[attrs.user.key])

    def balance(attrs, key: str):
        if attrs.user.key not in attrs.accounts:
            raise Exception('User holds no accounts')

        if key not in attrs.accounts[attrs.user.key]:
            raise Exception('Account not found')

        return attrs, str(attrs.accounts[attrs.user.key][key])

    contract = Builder('DigitalCurrency')
    contract.add_attribute('accounts', defaultdict(dict))
    contract.add_method(add_account)
    contract.add_method(increment)
    contract.add_method(transfer)
    contract.add_method(list_accounts)
    contract.add_method(balance)

    return contract

if __name__ == '__main__':
    application = make_tornado(ledger)
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
