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

from pyledger.server.status import BaseStatus, SimpleStatus


def test_1():
    status = SimpleStatus(key='value')
    assert isinstance(status, BaseStatus) == True
    assert ('key' in status) == True


def test_2():
    status = SimpleStatus(accounts={})
    status.accounts['My_account'] = 100
    assert status.accounts['My_account'] == 100


def test_serialization():
    status = SimpleStatus(accounts={})
    status.accounts['My_account'] = 100

    data = status.dump()
    del status

    status = SimpleStatus()
    status.load(data)

    assert status.accounts['My_account'] == 100
