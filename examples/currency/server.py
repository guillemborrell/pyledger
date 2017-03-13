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


def ledger():
    def add_account(attrs, key: str):
        if key in attrs.accounts:
            raise Exception('Account already exists')

        attrs.accounts[key] = 0.0
        return attrs

    def increment(attrs, key: str, quantity: float):
        if key not in attrs.accounts:
            raise Exception('Account not found')

        attrs.accounts[key] += quantity
        return attrs

    def transfer(attrs, source: str, dest: str, quantity: float):
        if source not in attrs.accounts:
            raise Exception('Source account not found')
        if dest not in attrs.accounts:
            raise Exception('Destination account not found')
        if attrs.accounts[source] < quantity:
            raise Exception('Not enough funds in source account')

        attrs.accounts[source] -= quantity
        attrs.accounts[dest] += quantity

        return attrs

    def balance(attrs, key: str):
        if key not in attrs.accounts:
            print(attrs.accounts)
            raise Exception('Account not found')

        return attrs, str(attrs.accounts[key])

    contract = Builder('DigitalCurrency')
    contract.add_property('accounts', {})
    contract.add_method(add_account)
    contract.add_method(increment)
    contract.add_method(transfer)
    contract.add_method(balance)

    return contract

if __name__ == '__main__':
    application = make_tornado(ledger)
    application.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()
