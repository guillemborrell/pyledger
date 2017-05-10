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

from pyledger.server import run
from pyledger.server.contract import SimpleContract


class DigitalCurrency(SimpleContract):
    accounts = {}

    def add_account(self, key: str):
        if key in self.accounts:
            raise Exception('Account already exists')

        self.accounts[key] = 0.0
        return key

    def increment(self, key: str, quantity: float):
        if key not in self.accounts:
            raise Exception('Account not found')

        self.accounts[key] += quantity

    def transfer(self, source: str, dest: str, quantity: float):
        if source not in self.accounts:
            raise Exception('Source account not found')
        if dest not in self.accounts:
            raise Exception('Destination account not found')
        if self.accounts[source] < quantity:
            raise Exception('Not enough funds in source account')
        if quantity < 0:
            raise Exception('You cannot transfer negative currency')

        self.accounts[source] -= quantity
        self.accounts[dest] += quantity

    def balance(self, key: str):
        if key not in self.accounts:
            print(self.accounts)
            raise Exception('Account not found')

        return str(self.accounts[key])


run(DigitalCurrency)